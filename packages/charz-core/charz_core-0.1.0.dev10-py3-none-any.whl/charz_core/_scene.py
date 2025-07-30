from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING, ClassVar, Any

from typing_extensions import Self

from ._frame_task import FrameTaskManager
from ._grouping import Group
from ._annotations import GroupID, NodeID

if TYPE_CHECKING:
    from ._node import Node


class SceneClassProperties(type):
    _current: Scene

    @property
    def current(cls) -> Scene:
        if not hasattr(cls, "_current"):
            cls._current = cls()  # Create default scene if none exists
        return cls._current

    @current.setter
    def current(cls, new: Scene) -> None:
        cls.current.on_exit()
        cls._current = new
        new.on_enter()


class Scene(metaclass=SceneClassProperties):
    """`Scene` to encapsulate dimensions/worlds

    When a node is created, it will be handled by the currently active `Scene`.
    If no `Scene` is created, a default `Scene` will be created and set as the active one

    By subclassing `Scene`, and implementing `__init__`, all nodes
    created in that `__init__` will be added to that subclass's group of nodes

    NOTE (Technical): A `Scene` hitting reference count of `0`
    will reduce the reference count to its nodes by `1`
    """

    # Tasks are shared across all scenes
    frame_tasks: ClassVar[FrameTaskManager[Self]] = FrameTaskManager()
    # Values are set in `Scene.__new__`
    nodes: list[Node]
    groups: defaultdict[GroupID, dict[NodeID, Node]]
    _queued_nodes: list[Node]

    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        instance = super().__new__(cls, *args, **kwargs)
        # NOTE: When instantiating the scene,
        #       it will be set as the current one
        #     - Use preloading to surpass
        Scene._current = instance
        instance.nodes = []
        instance.groups = defaultdict(dict)
        instance._queued_nodes = []
        return instance

    @classmethod
    def preload(cls) -> Self:
        previous_scene = Scene.current
        instance = cls()
        Scene.current = previous_scene
        return instance

    def __str__(self) -> str:
        group_counts = ", ".join(f"{group}: {len(self.groups[group])}" for group in Group)
        return f"{self.__class__.__name__}({group_counts})"

    def __init__(self) -> None:  # Override in subclass
        """Override to instantiate nodes and state related to this scene"""

    def set_current(self) -> None:
        Scene.current = self

    def as_current(self) -> Self:
        self.set_current()
        return self

    def get_group_members(self, group_id: GroupID, /) -> list[Node]:
        return list(self.groups[group_id].values())

    def get_first_group_member(self, group_id: GroupID, /) -> Node:
        for node in self.groups[group_id].values():
            return node
        raise ValueError(f"no node in group {group_id}")

    def process(self) -> None:
        for frame_task in self.frame_tasks.values():
            frame_task(self)

    def update(self) -> None:
        """Called each frame"""

    def on_enter(self) -> None:
        """Triggered when this scene is set as the current one"""

    def on_exit(self) -> None:
        """Triggered when this scene is no longer the current one"""


# Define frame tasks for `Scene`


def update_self(instance: Scene) -> None:
    instance.update()


def update_nodes(instance: Scene) -> None:
    # NOTE: `list` is faster than `tuple`, when copying
    # iterate a copy (hence the use of `list(...)`)
    # This allows node creation during iteration
    for node in list(instance.groups[Group.NODE].values()):
        node.update()


def free_queued_nodes(instance: Scene) -> None:
    for queued_node in instance._queued_nodes:
        queued_node._free()
    instance._queued_nodes *= 0  # Faster way to do `.clear()`


# Register frame tasks to `Scene` class
# Priorities are chosen with enough room to insert many more tasks in between
Scene.frame_tasks[100] = update_self
Scene.frame_tasks[90] = update_nodes
Scene.frame_tasks[80] = free_queued_nodes
