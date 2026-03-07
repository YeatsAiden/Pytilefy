import pygame as pg

from .camera import Camera
from .settings import *


class Grid(pg.sprite.Sprite):
    def __init__(self) -> None:
        pg.sprite.Sprite.__init__(self)
        self.image: pg.Surface = pg.Surface(DISPLAY_SIZE)
        self.rect: pg.FRect = pg.FRect()
        self.layer = 0

    def update(self, camera) -> None:
        self.image.fill("black")

        for y in range(int(camera.scroll.y)//TILE_SIZE, (int(camera.scroll.y) + DISPLAY_HEIGHT)//TILE_SIZE):
            pg.draw.line(self.image, (50, 50, 50), (0, y * TILE_SIZE - camera.scroll.y), (DISPLAY_WIDTH, y * TILE_SIZE - camera.scroll.y), 2)

        for x in range(int(camera.scroll.x)//TILE_SIZE, (int(camera.scroll.x) + DISPLAY_WIDTH)//TILE_SIZE):
            pg.draw.line(self.image, (50, 50, 50), (x * TILE_SIZE - camera.scroll.x, 0), (x * TILE_SIZE - camera.scroll.x, DISPLAY_HEIGHT), 2)

        pg.draw.line(self.image, (80, 80, 200), (0, 0 - camera.scroll.y), (DISPLAY_WIDTH, 0 - camera.scroll.y), 2)
        pg.draw.line(self.image, (200, 80, 80), (0 - camera.scroll.x, 0), (0 - camera.scroll.x, DISPLAY_HEIGHT), 2)

    def draw(self, surface: pg.Surface, scroll: pg.Vector2) -> None:
        surface.blit(self.image, (0, 0))
