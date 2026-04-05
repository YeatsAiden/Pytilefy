import pygame as pg

from .entity import Entity


# What a useless class, who would ever make a class like this one
class Sprite(Entity):
    def __init__(self, pos: pg.typing.Point, width, height) -> None:
        super().__init__()
        self.width = width
        self.height = height
        self.rect = pg.FRect(pos, width, height)
