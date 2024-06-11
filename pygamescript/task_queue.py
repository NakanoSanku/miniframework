import heapq
from threading import Lock
from typing import List, Optional, Tuple

from pygamescript.task import Task, TaskStatus, TaskProxy, BeforeTaskProxy


class TaskQueue:
    def __init__(self):
        self._task_queue: List[Tuple[int, Task | TaskProxy]] = []  # 优先队列
        self._lock = Lock()  # 用于线程安全
        self._current_task: Optional[Task | TaskProxy] = None

    @property
    def task_queue(self) -> List[Task | TaskProxy]:
        with self._lock:
            return [task for _, task in self._task_queue]

    @property
    def next_task(self) -> Optional[Task | TaskProxy]:
        with self._lock:
            while self._task_queue:
                _, task = heapq.heappop(self._task_queue)
                if task.status != TaskStatus.COMPLETED:
                    if self._current_task != task and isinstance(self._current_task, BeforeTaskProxy):
                        self._current_task.reset_proxy_task()
                    self._current_task = task
                    return task
        return None

    def __str__(self) -> str:
        with self._lock:
            tasks = [task for _, task in self._task_queue]
            return f"TaskQueue({len(tasks)} tasks: {tasks})"

    def add_task(self, task: Task, priority: int = 0):
        with self._lock:
            heapq.heappush(self._task_queue, (-priority, task))  # 负的优先级使得优先级大的任务优先

    def remove_task(self, task_uuid: str):
        with self._lock:
            self._task_queue = [t for t in self._task_queue if t[1].uuid != task_uuid]
            heapq.heapify(self._task_queue)  # 移除后重新堆化

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
