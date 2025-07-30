import threading
import ctypes
from concurrent.futures import ThreadPoolExecutor
from typing import Optional, TypeVar, Callable
from scan.common import logger

T = TypeVar('T')

class TimeoutThreadPool:
    """可终止的线程池管理器"""
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
            return cls._instance

    def __init__(self):
        if not hasattr(self, 'pool'):
            self.pool = ThreadPoolExecutor(
                max_workers=4,  # 默认工作线程数
                thread_name_prefix='timeout_worker'
            )
            self._running_threads = {}  # 存储正在运行的线程信息

    def submit_task(
        self,
        task: Callable[..., T],
        *args,
        timeout: int = 30,
        **kwargs
    ) -> Optional[T]:
        """
        提交任务到线程池并等待结果
        Args:
            task: 要执行的任务函数
            *args: 任务函数的位置参数
            timeout: 超时时间（秒）
            **kwargs: 任务函数的关键字参数
        Returns:
            任务执行结果，超时或失败返回None
        """
        result = {'value': None}
        done_event = threading.Event()
        thread_id = None

        def _wrapper():
            nonlocal thread_id
            # 记录当前线程
            current_thread = threading.current_thread()
            thread_id = current_thread.ident
            self._running_threads[thread_id] = current_thread

            try:
                result['value'] = task(*args, **kwargs)
            except (SystemExit, Exception) as e:
                if not isinstance(e, SystemExit):
                    logger.error(f"[timeout_pool] Task failed: {str(e)}")
                result['value'] = None
            finally:
                done_event.set()
                # 清理线程记录
                self._running_threads.pop(thread_id, None)

        try:
            # 提交任务到线程池
            self.pool.submit(_wrapper)

            # 等待任务完成或超时
            if done_event.wait(timeout=timeout):
                # 任务正常完成
                return result['value']
            else:
                # 任务超时，强制终止线程
                logger.error(f"[timeout_pool] Task timed out after {timeout} seconds")
                self._terminate_thread(thread_id)
                return None

        except Exception as e:
            logger.error(f"[timeout_pool] Failed to execute task: {str(e)}")
            return None

    def _terminate_thread(self, thread_id: Optional[int]):
        """终止指定的线程"""
        if thread_id and thread_id in self._running_threads:
            exc = ctypes.py_object(SystemExit)
            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
                ctypes.c_long(thread_id), exc)
            if res > 1:
                # 如果返回值大于1，说明出错了，尝试恢复
                ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread_id), None)

    def shutdown(self):
        """关闭线程池"""
        # 终止所有运行中的线程
        for thread_id in list(self._running_threads.keys()):
            self._terminate_thread(thread_id)
        # 关闭线程池
        self.pool.shutdown(wait=False)


# 创建全局超时线程池实例
timeout_pool = TimeoutThreadPool()
