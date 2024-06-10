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
    """任务代理抽象类"""

    def __init__(self, task: Task):
        super().__init__()
        self._task = task
        self._status = TaskStatus.PENDING  # 代理任务的状态

    @property
    def name(self) -> str:
        """任务名称"""
        return self._task.name

    @property
    def proxy_task_status(self) -> TaskStatus:
        return self._status

    @proxy_task_status.setter
    def proxy_task_status(self, status: TaskStatus):
        self._status = status

    @property
    def status(self) -> TaskStatus:
        return self._task.status

    def __str__(self) -> str:
        """任务描述"""
        return str(self._task)

    def reset(self):
        """重置任务状态"""
        self._task.reset()
        self.reset_proxy_task()

    @abstractmethod
    def reset_proxy_task(self):
        """
        重置代理任务状态
        将self.proxy_task_status设置成TaskStatus.PENDING
        """
        pass

    @abstractmethod
    def proxy_task(self):
        pass

    @abstractmethod
    def execute(self):
        pass


class BeforeTaskProxy(TaskProxy):
    """前置任务代理抽象类"""

    def __init__(self, task: Task):
        super().__init__(task)

    @abstractmethod
    def proxy_task(self):
        """
        前置任务逻辑实现
        任务完成后必须将self.proxy_task_status设置成TaskStatus.COMPLETED
        """
        pass

    def execute(self):
        """执行任务"""
        if self._status != TaskStatus.COMPLETED:
            self.proxy_task_status = TaskStatus.RUNNING
            self.proxy_task()
        else:
            self._task.execute()

    @abstractmethod
    def reset_proxy_task(self):
        """
        重置代理任务状态
        将self.proxy_task_status设置成TaskStatus.PENDING
        """
        pass


class AfterTaskProxy(TaskProxy):
    """后置任务代理抽象类"""

    def __init__(self, task: Task):
        super().__init__(task)

    @abstractmethod
    def proxy_task(self):
        """
        后置任务逻辑实现
        任务完成后必须将self.proxy_task_status设置成TaskStatus.COMPLETED
        """
        pass

    def execute(self):
        """执行任务"""
        if self.status == TaskStatus.COMPLETED:
            self.proxy_task_status = TaskStatus.RUNNING
            self.proxy_task()
        else:
            self._task.execute()

    @abstractmethod
    def reset_proxy_task(self):
        """
        重置代理任务状态
        将self.proxy_task_status设置成TaskStatus.PENDING
        """
        pass


class ExtraTaskProxy(TaskProxy):
    """任务增强代理抽象类"""

    def __init__(self, task: Task):
        super().__init__(task)

    @abstractmethod
    def proxy_task(self):
        """守护任务"""
        pass

    def execute(self):
        self.proxy_task()
        self._task.execute()
