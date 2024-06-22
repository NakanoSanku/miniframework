import time

from pygamescript import TaskStatus, TaskScheduler, Task, TaskQueue


class Task1(Task):
    def __init__(self, message: str):
        super().__init__()
        self._status = TaskStatus.PENDING
        self._message = message
        self._times = 5

    @staticmethod
    def name() -> str:
        return Task1.__name__

    @property
    def status(self) -> TaskStatus:
        return self._status

    def __str__(self) -> str:
        return self._message

    def task(self):
        if self._status == TaskStatus.PENDING:
            self._status = TaskStatus.RUNNING
        self._times -= 1

    def execute(self):
        self.task()
        if self._times == 0:
            self._status = TaskStatus.COMPLETED

    def reset(self):
        pass


task_queue = TaskQueue()  # 创建任务队列
task_queue.add_task(Task1(message="任务1,优先度为1"), priority=1)  # 向任务队列添加任务
task_scheduler = TaskScheduler(sleep_time=1000)  # 创建任务调度器
task_scheduler.task_queue = task_queue  # 将任务队列推送到任务调度器

task_scheduler.start()
time.sleep(2)
task_queue.add_task(Task1(message="任务2,优先度为2"), priority=2)  # 任务2
time.sleep(12)
task_queue.add_task(Task1(message="任务3,优先度为3"), priority=1)  # 任务2
task_scheduler.stop()
print(task_queue)
