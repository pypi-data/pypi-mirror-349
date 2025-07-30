from __future__ import annotations

from typing import TypeVar, TypeAlias, Generic, Callable

T = TypeVar("T")
Priority: TypeAlias = int
FrameTask: TypeAlias = Callable[[T], None]


class FrameTaskManager(Generic[T], dict[Priority, FrameTask[T]]):
    def __setitem__(self, key: int, value: Callable[[T], None]) -> None:
        super().__setitem__(key, value)
        # A higher priority means the callable will be called earlier
        sorted_items = sorted(self.items(), reverse=True)
        self.clear()
        self.update(sorted_items)
