from abc import ABC, abstractmethod
from enum import Enum, auto
from uuid import UUID, uuid4


class TaskStatus(Enum):
    PENDING = auto()
    RUNNING = auto()
    COMPLETED = auto()
    CANCELLED = auto()


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
    def before_task(self):
        """前置任务"""
        pass

    @abstractmethod
    def task(self):
        """实际任务"""
        pass

    @abstractmethod
    def after_task(self):
        """后置任务"""
        pass

    @abstractmethod
    def execute(self):
        """执行任务"""
        pass

    @abstractmethod
    def reset(self):
        """重置任务"""
        pass
