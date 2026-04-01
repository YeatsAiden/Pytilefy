import pygame as pg
from .renderer import Renderer


class Entity:
    def __init__(self) -> None:
        self.pos: pg.Vector2 = pg.Vector2()
        self.image: pg.Surface
        self.target: str = "window"
        self.z: int = 0

    @property
    def center(self) -> pg.typing.Point:
        return self.pos

    @center.setter
    def center(self, value: pg.typing.Point) -> None:
        self.pos.x, self.pos.y = value

    def update(self, *args, **kwargs) -> None:
        pass

    def blit(self, renderer: Renderer):
        renderer.blit(self.z, self.target, self.image, self.pos)

