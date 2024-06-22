from threading import Lock
from typing import List, Optional, Tuple

from miniframework.task import Task, TaskStatus, TaskProxy, BeforeTaskProxy


class TaskQueue:
    def __init__(self):
        self._task_queue: List[Tuple[int, Task | TaskProxy]] = []  # 优先队列
        self._lock = Lock()  # 用于线程安全
        self._current_task: Optional[Task | TaskProxy] = None

    @property
    def queue(self) -> List[Tuple[int, Task | TaskProxy]]:
        return self._task_queue

    @property
    def next_task(self) -> Optional[Task | TaskProxy]:
        for _, task in self._task_queue:
            if task.status != TaskStatus.COMPLETED:
                if self._current_task != task and isinstance(self._current_task, BeforeTaskProxy):
                    with self._lock:
                        self._current_task.reset_proxy_task()
                self._current_task = task
                return task
        return None

    def __str__(self) -> str:
        tasks = [str(task) for _, task in self._task_queue]
        return f"TaskQueue({len(tasks)} tasks: {tasks})"

    def add_task(self, task: Task, priority: int = 0):
        with self._lock:
            self._task_queue.append((priority, task))
            self._sort_task_queue()

    def remove_task(self, task_uuid: str):
        with self._lock:
            self._task_queue = [t for t in self._task_queue if t[1].uuid != task_uuid]

    def remove_all_tasks(self):
        with self._lock:
            self._task_queue.clear()

    def reset_task(self, task_uuid: str):
        with self._lock:
            for _, task in self._task_queue:
                if task.uuid == task_uuid:
                    task.reset()

    def reset_all_tasks(self):
        with self._lock:
            for _, task in self._task_queue:
                try:
                    task.reset()
                except Exception as e:
                    print(f"Failed to reset task {task.uuid}: {e}")

    def _sort_task_queue(self, reserve=True):
        self._task_queue.sort(key=lambda x: x[0], reverse=reserve)
