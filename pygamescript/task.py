from abc import ABC, abstractmethod
from enum import Enum, auto
from uuid import uuid4


class TaskStatus(Enum):
    PENDING = auto()
    RUNNING = auto()
    COMPLETED = auto()


class Task(ABC):
    def __init__(self):
        self._uuid = uuid4()

    @property
    def uuid(self) -> str:
        return str(self._uuid)

    @property
    @abstractmethod
    def name(self) -> str:
        """任务名称"""
        pass

    @property
    @abstractmethod
    def status(self) -> TaskStatus:
        """获取任务状态"""
        pass

    @abstractmethod
    def __str__(self) -> str:
        """任务描述信息"""
        pass

    @abstractmethod
    def task(self):
        """任务逻辑实现"""
        pass

    @abstractmethod
    def execute(self):
        """执行任务"""
        pass

    @abstractmethod
    def reset(self):
        """重置任务"""
        pass


class TaskProxy(Task):
    def __init__(self, task: Task):
        super().__init__()
        self._task = task
        self._status: TaskStatus = TaskStatus.PENDING

    @property
    def name(self) -> str:
        return self._task.name

    @property
    def status(self) -> TaskStatus:
        if self.proxy_status == TaskStatus.RUNNING or self._task.status == TaskStatus.RUNNING:
            return TaskStatus.RUNNING
        if self.proxy_status == TaskStatus.COMPLETED and self._task.status == TaskStatus.COMPLETED:
            return TaskStatus.COMPLETED
        return TaskStatus.PENDING

    @property
    def proxy_status(self) -> TaskStatus:
        return self._status

    @proxy_status.setter
    def proxy_status(self, status: TaskStatus):
        self._status = status

    def __str__(self) -> str:
        return self._task.__str__()

    def reset(self):
        self.reset_proxy_task()
        self._task.reset()

    @abstractmethod
    def task(self):
        pass

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def reset_proxy_task(self):
        pass


class BeforeTaskProxy(TaskProxy):
    def __init__(self, task: Task):
        super().__init__(task)
        self._task = task

    def execute(self):
        if self.proxy_status != TaskStatus.COMPLETED:
            self.task()
        else:
            self._task.execute()

    @abstractmethod
    def task(self):
        """
        前置任务
        完成后self._status = TaskStatus.COMPLETED
        """
        pass

    @abstractmethod
    def reset_proxy_task(self):
        """
        重置前置任务
        需将self._status = TaskStatus.PENDING
        """
        pass


class AfterTaskProxy(TaskProxy):
    def __init__(self, task: Task):
        super().__init__(task)
        self._task = task

    def execute(self):
        if self._task.status == TaskStatus.COMPLETED:
            self.task()
        else:
            self._task.execute()

    @abstractmethod
    def task(self):
        """
        后置任务
        完成后self._status = TaskStatus.COMPLETED
        """
        pass

    @abstractmethod
    def reset_proxy_task(self):
        """
        重置后置任务
        需将self._status = TaskStatus.PENDING
        """
        pass

