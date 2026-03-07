import pygame as pg
import json

from .settings import *
from .common import *
from .ui import *
from .level import Level


class Editor:
    def __init__(self, file_path: pg.typing.FileLike) -> None:
        self.level = Level(file_path)

    def place_tile(self, tile_pos_key: str):
        pass

    def delete_tile(self, tile_pos_key: str):
        pass

    def save_level(self):
        with open(self.level.file, "w") as f:
            json.dump(self.level, f)

    def auto_tile(self):
        pass

    def draw(self, surface: pg.Surface, scroll: pg.Vector2):
        self.level.draw(surface, scroll)
