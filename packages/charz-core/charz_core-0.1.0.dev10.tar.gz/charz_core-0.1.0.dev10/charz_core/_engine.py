from __future__ import annotations

from typing import ClassVar

from typing_extensions import Self

from ._frame_task import FrameTaskManager
from ._scene import Scene


class EngineMixinSorter(type):
    """Engine metaclass for initializing `Engine` subclass after other `mixin` classes"""

    def __new__(
        cls,
        name: str,
        bases: tuple[type, ...],
        attrs: dict[str, object],
    ) -> type:
        def sorter(base: type) -> bool:
            # TODO?: Add extra point for being the exact type `Engine`
            return isinstance(base, Engine)

        sorted_bases = tuple(sorted(bases, key=sorter))
        new_type = super().__new__(cls, name, sorted_bases, attrs)
        return new_type


class Engine(metaclass=EngineMixinSorter):
    # Tasks are shared across all engines
    frame_tasks: ClassVar[FrameTaskManager[Self]] = FrameTaskManager()
    # Using setter and getter to prevent subclass def overriding
    _is_running: bool = False

    @property
    def is_running(self) -> bool:
        return self._is_running

    @is_running.setter
    def is_running(self, run_state: bool) -> None:
        self._is_running = run_state

    def update(self) -> None:
        """Called each frame"""

    def run(self) -> None:  # Main loop function
        self.is_running = True
        while self.is_running:  # Main loop
            for frame_task in self.frame_tasks.values():
                frame_task(self)


# Define frame tasks for `Engine`


def update_self(instance: Engine) -> None:
    instance.update()


def process_current_scene(_instance: Engine) -> None:
    Scene.current.process()


# Register frame tasks to `Engine` class
# Priorities are chosen with enough room to insert many more tasks in between
Engine.frame_tasks[100] = update_self
Engine.frame_tasks[90] = process_current_scene
