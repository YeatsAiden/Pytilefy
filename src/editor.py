import pygame as pg
import json

from .camera import Camera
from .settings import *
from .common import *
from .ui import *
from .level import Level, tuple_to_json_coord


class Editor:
    def __init__(self, file_path: pg.typing.FileLike) -> None:
        self.level: Level = Level(file_path)

        # 21 is the single tile
        self.current_layer: int = 0

        self.spritesheet_id: str = ""
        self.tileset_id: str = ""

        self.is_visible = True
        self.has_collisions = True
        self.on_grid = True

    def place_tile(self, camera: Camera):
        tile_position = self.level.get_tile_coordinate_at(camera.mouse_pos_on_display)
        mouse_pressed = pg.mouse.get_pressed()

        if mouse_pressed[0]:
            if not self.level.level_data["layers"].get(self.current_layer):
                self.level.level_data["layers"][self.current_layer] = {}

            self.level.level_data["layers"][self.current_layer][(tile_position.x, tile_position.y)] = {
                "type": "tile",
                "id": 0,
                "spritesheet_id": "grass",
            }

    def delete_tile(self, tile_pos_key: str):
        pass

    def save_level(self):
        with open(self.level.file, "w") as f:
            level = self.level.level_data.copy()
            for layer in level["layers"].values():
                layer["tiles"] = {tuple_to_json_coord(k): v for k, v in layer["tiles"].items()}
            json.dump(level, f)

    def auto_tile(self):
        pass

    def draw(self, surface: pg.Surface, scroll: pg.Vector2):
        self.level.draw(surface, scroll)
