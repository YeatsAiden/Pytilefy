import pygame as pg
from pathlib import Path
import json

from . import settings
from .camera import Camera
from .level import Level, tuple_to_json_coord


class Editor:
    def __init__(self, file_path: Path) -> None:
        self.level: Level = Level(file_path)
        settings.TILE_SIZE = self.level.level_data["tile_size"]
        settings.CHUNK_SIZE = self.level.level_data["chunk_size"]

        # 21 is the single tile
        self.current_layer: int = 0

        self.spritesheet_id: str = ""
        self.tileset_id: str = ""

        self.is_visible = True
        self.has_collisions = True
        self.on_grid = True

    def place_tile(self, camera: Camera):
        tile_position = self.level.get_tile_pos_at(camera.mouse_pos_on_display)
        mouse_pressed = pg.mouse.get_pressed()

        if mouse_pressed[0]:
            chunk_position = (tile_position.x//settings.CHUNK_SIZE, tile_position.y//settings.CHUNK_SIZE)

            if not self.level.level_data["layers"].get(self.current_layer):
                self.level.level_data["layers"][self.current_layer] = {}
                # if not self.level.level_data["layers"][self.current_layer][].get():
                #     self.level.level_data["layers"][self.current_layer][] = {}

            self.level.level_data["layers"][self.current_layer][chunk_position][tile_position] = {
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
