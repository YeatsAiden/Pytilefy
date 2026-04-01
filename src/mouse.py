import pygame as pg

from .assets import images
from .entity import Entity
from .renderer import Renderer

class Mouse(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.image: pg.Surface = images["cursor"]
        self.rect: pg.FRect = self.image.get_frect()
        self.z = 100

    def update(self) -> None:
        self.pos.x, self.pos.y = pg.mouse.get_pos()
        self.rect.center = self.pos

    def blit(self, renderer: Renderer) -> None:
        self.pos.x, self.pos.y = self.rect.center
        super().blit(renderer)
        self.pos.x, self.pos.y = self.rect.topleft
