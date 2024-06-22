# Task Proxy Design Documentation

## Overview

This document details the implementation of a Task Proxy system using Python's Abstract Base Classes (ABC) and Enum. The system allows for creating and managing tasks with various proxy types that modify or enhance the execution of these tasks.

## Components

### Enums

#### TaskStatus

An enumeration to represent the status of a task.

```python
from enum import Enum, auto

class TaskStatus(Enum):
    PENDING = auto()
    RUNNING = auto()
    COMPLETED = auto()
```

- **PENDING**: Indicates the task is pending.
- **RUNNING**: Indicates the task is currently running.
- **COMPLETED**: Indicates the task has been completed.

### Abstract Base Classes

#### Task

The base class for all tasks. This class is abstract and cannot be instantiated directly.

```python
from abc import ABC, abstractmethod
from uuid import uuid4

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
```

- **uuid**: Returns the unique identifier of the task.
- **name**: Abstract property for the name of the task.
- **status**: Abstract property for the status of the task.
- **task()**: Abstract method for implementing the task logic.
- **execute()**: Abstract method for executing the task.
- **reset()**: Abstract method for resetting the task.

#### TaskProxy

A base class for task proxies. This class is also abstract.

```python
class TaskProxy(Task):
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
```

- **proxy_task_status**: Property to get or set the proxy task status.
- **reset_proxy_task()**: Abstract method to reset the proxy task status.
- **proxy_task()**: Abstract method for the proxy task logic.
- **execute()**: Abstract method to execute the proxy task and the main task.

### Proxy Classes

#### BeforeTaskProxy

A proxy class for tasks that need a pre-execution logic.

```python
class BeforeTaskProxy(TaskProxy):
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
```

- **proxy_task()**: Abstract method for pre-execution logic. Must set `self.proxy_task_status` to `TaskStatus.COMPLETED` upon completion.
- **execute()**: Executes the proxy task if not completed; otherwise, executes the main task.

#### AfterTaskProxy

A proxy class for tasks that need a post-execution logic.

```python
class AfterTaskProxy(TaskProxy):
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
```

- **proxy_task()**: Abstract method for post-execution logic. Must set `self.proxy_task_status` to `TaskStatus.COMPLETED` upon completion.
- **execute()**: Executes the proxy task if the main task is completed; otherwise, executes the main task.

#### ExtraTaskProxy

A proxy class for tasks that need additional or enhanced logic.

```python
class ExtraTaskProxy(TaskProxy):
    def __init__(self, task: Task):
        super().__init__(task)

    @abstractmethod
    def proxy_task(self):
        """守护任务"""
        pass

    def execute(self):
        self.proxy_task()
        self._task.execute()
```

- **proxy_task()**: Abstract method for additional task logic.
- **execute()**: Executes the proxy task logic before executing the main task.

## Usage

To use these classes, you need to define concrete implementations of `Task` and any desired proxy class. Here is an example:

```python
class ConcreteTask(Task):
    def __init__(self):
        super().__init__()
        self._status = TaskStatus.PENDING

    @property
    def name(self) -> str:
        return "Concrete Task"

    @property
    def status(self) -> TaskStatus:
        return self._status

    def task(self):
        # Task logic here
        pass

    def execute(self):
        self._status = TaskStatus.RUNNING
        self.task()
        self._status = TaskStatus.COMPLETED

    def reset(self):
        self._status = TaskStatus.PENDING

    def __str__(self) -> str:
        return f"Task {self.name} with UUID {self.uuid}"

class ConcreteBeforeTaskProxy(BeforeTaskProxy):
    def proxy_task(self):
        # Pre-execution logic here
        self.proxy_task_status = TaskStatus.COMPLETED

    def reset_proxy_task(self):
        self.proxy_task_status = TaskStatus.PENDING

# Usage
task = ConcreteTask()
proxy = ConcreteBeforeTaskProxy(task)
proxy.execute()
```

In this example, `ConcreteTask` is a concrete implementation of the `Task` class, and `ConcreteBeforeTaskProxy` is a concrete implementation of the `BeforeTaskProxy` class.