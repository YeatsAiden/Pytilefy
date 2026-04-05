import pygame as pg

from .assets import images
from .entity import Entity
from .sprite import Sprite
from .entity_group import EntityGroup
from .renderer import Renderer

class Mouse(Entity):
    def __init__(self, ui_elements: EntityGroup) -> None:
        super().__init__()
        self.ui_elements = ui_elements
        self.image: pg.Surface = images["cursor"]
        self.rect: pg.FRect = self.image.get_frect()
        self.z = 100

    # @property
    # def over_element(self) -> Sprite:
    #     for ui_element in self.ui_elements:
    #         return ui_element

    def update(self) -> None:
        self.pos.x, self.pos.y = pg.mouse.get_pos()
        self.rect.center = self.pos

    def select(self) -> None:
        self.pos.x, self.pos.y = pg.mouse.get_pos()
        self.rect.center = self.pos

    def blit(self, renderer: Renderer) -> None:
        self.pos.x, self.pos.y = self.rect.center
        super().blit(renderer)
        self.pos.x, self.pos.y = self.rect.topleft
