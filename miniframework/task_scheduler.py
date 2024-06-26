import threading
import time
from enum import Enum, auto
from typing import Optional

from loguru import logger

from miniframework.task_queue import TaskQueue

SLEEP_TIME = 0


# 任务调度器状态
class TaskSchedulerStatus(Enum):
    PENDING = auto()
    RUNNING = auto()
    PAUSED = auto()


class TaskScheduler:
    def __init__(self, sleep_time: int = SLEEP_TIME):
        """
        :param sleep_time:任务执行间隔时间,单位为ms
        """
        self._task_queue: Optional[TaskQueue] = None
        self._work_thread: Optional[threading.Thread] = None
        self._status = TaskSchedulerStatus.PENDING
        self._sleep_time = sleep_time / 1000

    @property
    def task_queue(self) -> TaskQueue:
        return self._task_queue

    @task_queue.setter
    def task_queue(self, task_queue: TaskQueue):
        self._task_queue = task_queue

    @property
    def status(self) -> TaskSchedulerStatus:
        return self._status

    def __str__(self) -> str:
        return f"TaskScheduler(status={self._status}, task_queue={self._task_queue})"

    def _run(self):
        """任务调度器线程运行的内部方法"""
        while self.status == TaskSchedulerStatus.RUNNING:
            next_task = self._task_queue.next_task if self._task_queue else None
            if next_task:
                logger.debug(f"Executing task: {next_task}")
                next_task.execute()
            else:
                logger.debug(f"Task queue is empty,Waiting {self._sleep_time} seconds")
            time.sleep(self._sleep_time)

    def start(self):
        """启动任务调度器"""
        if self._task_queue is None:
            raise ValueError("Task queue must be set before starting the scheduler.")
        if self._status == TaskSchedulerStatus.RUNNING:
            raise RuntimeError("Scheduler is already running.")
        self._status = TaskSchedulerStatus.RUNNING
        self._work_thread = threading.Thread(target=self._run)
        self._work_thread.start()
        logger.debug("TaskScheduler started.")

    def stop(self):
        """停止任务调度器"""
        if self.status == TaskSchedulerStatus.PENDING:
            return
        self._status = TaskSchedulerStatus.PENDING
        if self._work_thread:
            self._work_thread.join()
        self._task_queue.reset_all_tasks()  # 重置所有任务状态
        logger.debug("TaskScheduler stopped.")

    def pause(self):
        if self.status != TaskSchedulerStatus.RUNNING:
            return
        self._status = TaskSchedulerStatus.PAUSED
        if self._work_thread:
            self._work_thread.join()
        logger.debug("TaskScheduler paused.")

