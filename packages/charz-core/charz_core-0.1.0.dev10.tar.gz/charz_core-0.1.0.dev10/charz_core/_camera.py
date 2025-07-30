from __future__ import annotations

from enum import Flag, unique, auto
from typing import Literal

from linflex import Vec2
from typing_extensions import Self

from ._node import Node, NodeMixinSorter
from ._prefabs._node2d import Node2D


@unique
class CameraMode(Flag):
    FIXED = auto()
    CENTERED = auto()
    INCLUDE_SIZE = auto()


class CameraClassAttributes(NodeMixinSorter):
    MODE_FIXED: CameraMode = CameraMode.FIXED
    MODE_CENTERED: CameraMode = CameraMode.CENTERED
    MODE_INCLUDE_SIZE: CameraMode = CameraMode.INCLUDE_SIZE
    _current: Camera

    @property
    def current(self) -> Camera:
        if not hasattr(self, "_current"):
            self._current = Camera()  # Create default camera if none exists
        return self._current

    @current.setter
    def current(self, new: Camera) -> None:
        self._current = new


class Camera(Node2D, metaclass=CameraClassAttributes):
    """`Camera` for controlling location of viewport in the world, per `Scene`

    A default `Camera` will be used if not explicitly set
    """

    mode: CameraMode = CameraMode.FIXED

    def __init__(
        self,
        parent: Node | None = None,
        *,
        position: Vec2 | None = None,
        rotation: float | None = None,
        top_level: bool | None = None,
        mode: CameraMode | None = None,
        current: Literal[True] | None = None,
    ) -> None:
        if parent is not None:
            self.parent = parent
        if position is not None:
            self.position = position
        if rotation is not None:
            self.rotation = rotation
        if top_level is not None:
            self.top_level = top_level
        if mode is not None:
            self.mode = mode
        if current is True:
            self.set_current()

    def set_current(self) -> None:
        Camera.current = self

    def as_current(self) -> Self:
        self.set_current()
        return self

    def is_current(self) -> bool:
        return Camera.current is self

    def with_mode(self, mode: CameraMode, /) -> Self:
        self.mode = mode
        return self
