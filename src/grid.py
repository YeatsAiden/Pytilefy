import pygame as pg

from .camera import Camera
from .settings import *
from .entity import Entity


class Grid(Entity):
    def __init__(self, camera: Camera) -> None:
        super().__init__()
        self.camera = camera
        self.image: pg.Surface = pg.Surface(DISPLAY_SIZE)
        self.target = "display"
        self.z = -1

    def update(self) -> None:
        self.image.fill("black")

        for y in range(int(self.camera.scroll.y)//TILE_SIZE[1], (int(self.camera.scroll.y) + DISPLAY_HEIGHT)//TILE_SIZE[1] + 1):
            pg.draw.line(self.image, (50, 50, 50), (0, y * TILE_SIZE[1] - self.camera.scroll.y), (DISPLAY_WIDTH, y * TILE_SIZE[1] - self.camera.scroll.y), 2)

        for x in range(int(self.camera.scroll.x)//TILE_SIZE[0], (int(self.camera.scroll.x) + DISPLAY_WIDTH)//TILE_SIZE[0] + 1):
            pg.draw.line(self.image, (50, 50, 50), (x * TILE_SIZE[0] - self.camera.scroll.x, 0), (x * TILE_SIZE[0] - self.camera.scroll.x, DISPLAY_HEIGHT), 2)

        pg.draw.line(self.image, (80, 80, 200), (0, 0 - self.camera.scroll.y), (DISPLAY_WIDTH, 0 - self.camera.scroll.y), 2)
        pg.draw.line(self.image, (200, 80, 80), (0 - self.camera.scroll.x, 0), (0 - self.camera.scroll.x, DISPLAY_HEIGHT), 2)

