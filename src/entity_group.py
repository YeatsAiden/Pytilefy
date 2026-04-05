import pygame as pg

from .entity import Entity
from .renderer import Renderer

class EntityGroup:
    def __init__(self, *entities: Entity) -> None:
        self.entities: list[Entity] = entities

    def blit(self, renderer: Renderer) -> None:
        for entity in self.entities:
            entity.blit(renderer)

    def __iter__(self):
        for entity


