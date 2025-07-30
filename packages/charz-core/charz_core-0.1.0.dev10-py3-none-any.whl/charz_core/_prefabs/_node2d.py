from __future__ import annotations as _annotations

from linflex import Vec2

from .._node import Node
from .._components._transform import TransformComponent


class Node2D(TransformComponent, Node):
    def __init__(
        self,
        parent: Node | None = None,
        *,
        position: Vec2 | None = None,
        rotation: float | None = None,
        top_level: bool | None = None,
    ) -> None:
        super().__init__(parent=parent)
        if position is not None:
            self.position = position
        if rotation is not None:
            self.rotation = rotation
        if top_level is not None:
            self.top_level = top_level

    def __str__(self) -> str:
        return (
            self.__class__.__name__
            + "("
            + f"#{self.uid}"
            + f":{round(self.position, 2)}"
            + f":{round(self.rotation, 2)}R"
            + ")"
        )
