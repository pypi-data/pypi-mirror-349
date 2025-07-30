import json
import asyncio
import random
from typing import List, Callable, Awaitable, Optional, Any, Tuple
import aio_pika
from aio_pika import DeliveryMode
from aio_pika.pool import Pool
from aio_pika.exceptions import QueueEmpty
from scan.common import logger
from json import JSONDecodeError


class RandomConnectionPool:
    def __init__(
        self,
        constructor: Callable[..., Awaitable[Any]],
        *args: Any,
        max_size: Optional[int] = None,
    ):
        self._constructor = constructor
        self._constructor_args: Tuple[Any, ...] = args
        self._max_size = max_size
        self._created = 0
        self._items: List[Any] = []
        self._item_set: set = set()
        self._lock = asyncio.Lock()
        self._closed = False

    async def acquire(self):
        if self._closed:
            raise RuntimeError("Pool is closed")

        async with self._lock:
            # 如果池中有已释放的，随机返回一个
            if self._items:
                index = random.randint(0, len(self._items) - 1)
                return self._items.pop(index)

            # 没有空闲连接并且已达到最大创建数量
            if self._max_size is not None and self._created >= self._max_size:
                raise RuntimeError("Connection pool overflow")

            # 创建新连接
            item = await self._constructor(*self._constructor_args)
            self._created += 1
            self._item_set.add(item)
            return item

    async def release(self, item):
        if self._closed:
            try:
                await item.close()
            except Exception:
                pass
            return

        async with self._lock:
            self._items.append(item)

    async def close(self):
        self._closed = True
        async with self._lock:
            for item in self._item_set:
                try:
                    await item.close()
                except Exception:
                    pass
            self._items.clear()
            self._item_set.clear()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


class RabbitMQ:
    def __init__(self, **kwargs):
        self.host = kwargs.get('host') or 'localhost'
        self.port = kwargs.get('port') or 5672
        self.user = kwargs.get('user') or 'root'
        self.password = kwargs.get('password') or 'root'
        self.virtualhost = kwargs.get('virtualhost') or '/'
        self.max_connection_size = kwargs.get('max_connection_size') or 1
        self.connection_pool = None
        self.channel_pool = None
        self.lock = asyncio.Lock()

    async def _create_pool(self):
        async def _get_connection():
            connection = await aio_pika.connect_robust(host=self.host, port=int(self.port), login=self.user,
                                                       password=self.password, virtualhost=self.virtualhost)
            return connection
        async with self.lock:
            if not self.connection_pool:
                self.connection_pool = RandomConnectionPool(_get_connection, max_size=int(self.max_connection_size))

        async def _get_channel():
            connection = await self.connection_pool.acquire()
            if connection.is_closed:
                await connection.reconnect()
            return await connection.channel()

        async with self.lock:
            if not self.channel_pool:
                self.channel_pool = Pool(_get_channel, max_size=int(self.max_connection_size) * 50)

    async def get_channel(self):
        for _ in range(3):
            try:
                async with self.channel_pool.acquire() as channel:
                    if channel.is_closed:
                        await channel.reopen()
                    return channel
            except Exception as e:
                logger.error(f'get channel error:{e}')

    async def init(self, max_channel_size=None):
        # if max_channel_size and isinstance(max_channel_size, int):
        #     self.max_channel_size = max_channel_size
        await self._create_pool()

    async def consume(self, call_back,  queue_name, no_ack=False, auto_ack=False, durable=True, auto_delete=False,
                      arguments=None, qos=1):
        """
        :param call_back: 回调函数
        :param qos:
        :param auto_delete:
        :param durable:
        :param no_ack:
        :param auto_ack: 拿到消息确认后再执行之后的逻辑
        :param arguments: mq绑定参数
        :param queue_name: 队列名
        :return:
        """
        try:
            channel = await self.get_channel()
            await channel.set_qos(qos)
            queue = await channel.declare_queue(queue_name, durable=durable, arguments=arguments,
                                                auto_delete=auto_delete)
            feedback = {}
            async with queue.iterator(no_ack=no_ack) as queue_iter:
                async for message in queue_iter:
                    body = message.body
                    try:
                        task_info = json.loads(body.decode())
                        task_info.update(feedback)
                    except JSONDecodeError:
                        logger.error(f'Description Failed to format task data:{body}')
                        await message.ack()
                        continue
                    if auto_ack:
                        await message.ack()
                    try:
                        pres = await call_back(task_info)
                    except Exception as e:
                        logger.error(f'consume error:{e}')
                    if pres:
                        if not auto_ack:
                            await message.ack()
                        if isinstance(pres, dict):
                            feedback = pres
                    else:
                        logger.error(f'task fail, resend data:{task_info}')
                        priority = message.priority
                        await self.publish(data=task_info, routing_key=queue_name, priority=priority)
                        if not auto_ack:
                            await message.ack()
        except Exception as e:
            logger.error(f'consume process error: {e}')

    async def get_message(self, queue_name, durable=True, auto_delete=False, arguments=None, timeout=10):
        try:
            channel = await self.get_channel()
            queue = await channel.declare_queue(queue_name, durable=durable, arguments=arguments,
                                                auto_delete=auto_delete)
            message = await queue.get(no_ack=True, timeout=timeout)
            if not message:
                return
            body = message.body
            try:
                task_info = json.loads(body.decode())
                return task_info
            except JSONDecodeError:
                logger.error(f'Description Failed to format task data:{body}')
            return
        except QueueEmpty:
            return
        except Exception as e:
            logger.error(f'get message error: {e}')

    async def publish(self, data, routing_key, priority=None, channel=None, delivery_mode=DeliveryMode.PERSISTENT):
        """
        :param delivery_mode: 默认开启持久化
        :param priority: 消息优先级
        :param data: 要发送的数据
        :param routing_key: 队列名
        :param channel: 通道
        :return:
        """
        try:
            if not channel:
                channel = await self.get_channel()
                try:
                    await channel.default_exchange.publish(aio_pika.Message(body=json.dumps(data).encode(),
                                                                            delivery_mode=delivery_mode,
                                                                            priority=priority),
                                                           routing_key=routing_key)
                    return True
                except Exception as e:
                    logger.error(f'publish error: {e}')
            else:
                try:
                    await channel.default_exchange.publish(aio_pika.Message(body=json.dumps(data).encode(),
                                                                            delivery_mode=delivery_mode,
                                                                            priority=priority),
                                                           routing_key=routing_key)
                    return True
                except Exception as e:
                    logger.error(f'publish error: {e}')
        except Exception as e:
            logger.error(f'publish process error: {e}')

    async def purge(self, queue_name, arguments=None):
        """
        :param arguments: 绑定队列参数
        :param queue_name: 要清空的队列名
        :return:
        """
        try:
            channel = await self.get_channel()
            try:
                queue = await channel.declare_queue(queue_name, durable=True, arguments=arguments,
                                                    auto_delete=False)
                await queue.purge()
                return True
            except Exception as e:
                logger.error(f'purge error: {e}')
        except Exception as e:
            logger.error(f'purge process error: {e}')

    async def message_count(self, queue_name, arguments=None):
        try:
            channel = await self.get_channel()
            try:
                queue = await channel.declare_queue(queue_name, durable=True, arguments=arguments,
                                                    auto_delete=False)
                count = queue.declaration_result.message_count
                return count
            except Exception as e:
                logger.error(f'message_count error: {e}')
        except Exception as e:
            logger.error(f'message_count process error: {e}')


__all__ = RabbitMQ
