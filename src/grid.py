import pygame as pg

from camera import Camera
from .settings import *


class Grid(pg.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.image: pg.Surface = pg.Surface(DISPLAY_SIZE)

    def update(self, camera) -> None:
        y_range = (int(camera.view_rect.y) + DISPLAY_HEIGHT)//TILE_SIZE - int(camera.view_rect.y)//TILE_SIZE + 1
        x_range = (int(camera.view_rect.x) + DISPLAY_WIDTH)//TILE_SIZE - int(camera.view_rect.x)//TILE_SIZE + 1

        for y in range(y_range):
            pg.draw.line(self.image, (50, 50, 50), (0, y * TILE_SIZE - camera.scroll.y), (DISPLAY_WIDTH, y * TILE_SIZE - camera.scroll.y), 2)

        for x in range(x_range):
            pg.draw.line(self.image, (50, 50, 50), (x * TILE_SIZE - camera.scroll.x, 0), (x * TILE_SIZE - camera.scroll.x, DISPLAY_HEIGHT), 2)

        pg.draw.line(self.image, (80, 80, 200), (0, 0 - camera.scroll.y), (DISPLAY_WIDTH, 0 - camera.scroll.y), 2)
        pg.draw.line(self.image, (200, 80, 80), (0 - camera.scroll.x, 0), (0 - camera.scroll.x, DISPLAY_HEIGHT), 2)

    def draw(self, surface: pg.Surface, scroll: pg.Vector2) -> None:
        surface.blit(self.image, (0, 0))
