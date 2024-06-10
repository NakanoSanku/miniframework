from typing import List, Optional
from threading import Lock
from pygamescript.task import Task, TaskStatus


class TaskQueue:
    def __init__(self):
        self._task_queue: List[Task] = []  # 初始化任务队列
        self._lock = Lock()  # 用于线程安全

    @property
    def task_queue(self) -> List[Task]:
        return self._task_queue

    @property
    def next_task(self) -> Optional[Task]:
        with self._lock:
            for task in self._task_queue:
                if task.status != TaskStatus.COMPLETED:
                    return task
        return None

    def __str__(self) -> str:
        with self._lock:
            return f"TaskQueue({len(self._task_queue)} tasks: {self._task_queue})"

    def add_task(self, task: Task):
        with self._lock:
            self._task_queue.append(task)

    def remove_task(self, task_uuid: str):
        with self._lock:
            self._task_queue = [task for task in self._task_queue if task.uuid != task_uuid]

    def remove_all_tasks(self):
        with self._lock:
            self._task_queue.clear()

    def reset_task(self, task_uuid: str):
        with self._lock:
            for task in self._task_queue:
                if task.uuid == task_uuid:
                    task.reset()

    def reset_all_tasks(self):
        with self._lock:
            for task in self._task_queue:
                try:
                    task.reset()
                except Exception as e:
                    print(f"Failed to reset task {task.uuid}: {e}")
