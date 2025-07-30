import asyncio
from abc import ABCMeta
from scan.core.spiders.spider import Spider
from scan import logger


class TrackableQueue(asyncio.Queue):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._unfinished_tasks = 0  # 用于追踪未完成任务数

    async def put(self, item):
        """放入任务时增加未完成任务计数"""
        await super().put(item)
        self._unfinished_tasks += 1

    async def get(self):
        """取出任务，未完成任务数不变"""
        return await super().get()

    def task_done(self):
        """任务完成后减少未完成任务计数"""
        if self._unfinished_tasks <= 0:
            raise ValueError("task_done() called too many times")
        super().task_done()
        self._unfinished_tasks -= 1

    def unfinished_tasks(self):
        """返回未完成任务数，python3.8之前是存在的"""
        return self._unfinished_tasks



class SimpleSpider(Spider, metaclass=ABCMeta):

    task_queue = TrackableQueue()

    async def add_url(self, url: str):
        """
        把下次需要请求的url放入队列
        """
        await self.task_queue.put({'url': url})

    async def add_task(self, task_info: dict):
        """
        添加任务对象
        """
        await self.task_queue.put(task_info)

    async def init(self):
        """
        普通抓取不要求初始化配置
        """

    async def _task(self):
        _next = None
        while (self.spider_status == 'running' and not self.task_queue.empty() and
               self.task_queue.unfinished_tasks() > 0):
            try:
                if self.task_queue.empty():
                    await asyncio.sleep(0.1)
                    continue
                try:
                    task_info = self.task_queue.get_nowait()
                    if _next:
                        task_info.update({'_next': _next})
                except asyncio.QueueEmpty:
                    continue
                try:
                    res = await self._process(task_info)
                    if isinstance(res, dict):
                        _next = res
                    else:
                        _next = None
                finally:
                    self.task_queue.task_done()  # 减少队列计数
            except Exception as e:
                logger.error(e)
