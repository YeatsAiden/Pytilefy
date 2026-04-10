import pygame as pg
from pathlib import Path
import json

from . import settings
from .camera import Camera
from .level import Level, tuple_to_json_pos, convert_pos_to

#FIXME: Fix the reason for levels being saved improperly

class Editor:
    def __init__(self, file_path: Path, camera: Camera) -> None:
        self.level: Level = Level(file_path, camera)
        settings.TILE_SIZE = self.level.level_data["tile_size"]
        settings.CHUNK_SIZE = self.level.level_data["chunk_size"]

        self.camera = camera

        # 21 is the single tile
        self.current_layer: int = 0

        self.tile_type = "tile"
        self.spritesheet_id: str = "default"
        self.tile_id = 0
        self.tile_off_set = [0, 0]

        # Tile anatomy
        # (x, y): "type" "id" "spritesheet_id" "off_set" (for tiles that don't exactly fit the grid)

        self.is_visible = True
        self.has_collisions = True
        self.on_grid = True

    def place_tile(self):
        mouse_pressed = pg.mouse.get_pressed()
        mouse_pos = self.camera.mouse_pos_in_world

        if mouse_pressed[0]:
            tile_pos = self.level.get_tile_pos_at(*mouse_pos) if self.on_grid else mouse_pos
            chunk_pos = self.level.get_chunk_pos_at(*tile_pos)

            # Is checking for non-existing layers/chunks
            current_layer = self.level.level_data["layers"].get(self.current_layer)
            if not current_layer:
                self.level.level_data["layers"][self.current_layer] = {
                        "chunks": {},
                        "is_visible": True,
                        "has_collisions": True,
                        }

            current_chunk = self.level.level_data["layers"][self.current_layer]["chunks"].get(chunk_pos)
            if not current_chunk:
                self.level.level_data["layers"][self.current_layer]["chunks"][chunk_pos] = {}

            self.level.level_data["layers"][self.current_layer]["chunks"][chunk_pos][tile_pos] = {
                    "type": self.tile_type,
                    "id": self.tile_id,
                    "spritesheet_id": self.spritesheet_id,
                    }

    def delete_tile(self):
        mouse_pressed = pg.mouse.get_pressed()
        mouse_pos = self.camera.mouse_pos_in_world

        if mouse_pressed[2]:
            tile_pos = self.level.get_tile_pos_at(*mouse_pos)
            chunk_pos = self.level.get_chunk_pos_at(*tile_pos)

            # Is checking for non-existing layers/chunks/tiles
            current_layer = self.level.level_data["layers"].get(self.current_layer)
            if not current_layer:
                return

            current_chunk = current_layer["chunks"].get(chunk_pos)
            if not current_chunk:
                return

            current_tile = current_chunk.get(tile_pos)
            if not current_tile:
                return

            current_tile = current_chunk.pop(tile_pos)

    def save_level(self):
        with open(self.level.file, "w") as f:
            level = self.level.level_data.copy()
            convert_pos_to(level, tuple_to_json_pos)
            json.dump(level, f)

    def auto_tile(self):
        pass
