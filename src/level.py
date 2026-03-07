from os import wait
import pygame as pg
import json

from .settings import *
from .assets import images
from .common import *


class Level:
    def __init__(self, file_path: pg.typing.FileLike) -> None:
        self.file = str(file_path) + ".json"
        self.level = {
            "layers": {},
            "height": 0,
            "width": 0,
        }

        try:
            with open(self.file, "r") as f:
                self.level = json.load(f)
        except:
            with open(self.file, "w") as f:
                json.dump(self.level, f)

        self.rects = self.get_level_rects()
        self.tiles = {layer_id: set(layer) for layer_id, layer in self.level["layers"].items()}
        self.layer_ids = sorted(list(self.level["layers"].keys()), key= lambda x: int(x))

    def get_tile_coordinate(self, point: pg.Vector2) -> pg.Vector2:
        return pg.Vector2(point.x//TILE_SIZE, point.y//TILE_SIZE)

    def get_level_rects(self):
        rects = {}
        height = self.level["height"]
        width = self.level["width"]
        visited = {f"{j};{i}": False for i in range(height) for j in range(width)}

        for layer in self.level["layers"].values():
            if not layer["collide"]:
                continue

            for i in range(height):
                for j in range(width):
                    tile_pos = f"{j};{i}"
                    if visited[tile_pos] or not layer.get(tile_pos):
                        visited[tile_pos] = True
                        continue

                    rect_width = 1
                    rect_height = 1

                    while rect_width + j < width and layer.get(f"{j + rect_width};{i}") and not visited[f"{j + rect_width};{i}"]:
                        rect_width += 1

                    while i + rect_height < height:
                        valid = True
                        k = j
                        while k < j + rect_width:
                            if visited[f"{i + rect_height};{k}"] or not layer.get(f"{i + rect_height};{k}"):
                                valid = False
                                break
                            k += 1
                        if not valid:
                            break
                        rect_height += 1

                    for k in range(i, i + rect_height):
                        for l in range(j, j +rect_width):
                            visited[f"{l};{k}"] = True

                    # Real cursed
                    rects.update(dict.fromkeys([f"{l};{k}" for k in range(i, i + rect_height) for l in range(j, j +rect_width)], pg.FRect(j, i, rect_width, rect_height)))

        return rects

    def get_area(self, scroll: pg.Vector2):
        area = {}

        start_row = int(scroll[1] // TILE_SIZE)
        end_row = int((scroll[1] + DISPLAY_HEIGHT) // TILE_SIZE) + 1
        start_col = int(scroll[0] // TILE_SIZE)
        end_col = int((scroll[0] + DISPLAY_WIDTH) // TILE_SIZE) + 1

        positions = {f"{x}:{y}" for y in range(start_row, end_row + 1) for x in range(start_col, end_col + 1)}

        for layer in self.level:
            area[layer] = positions & self.tiles[layer]

        return area

    def draw(self, surface: pg.Surface, scroll: pg.Vector2):
        area = self.get_area(scroll)
        for layer_id in self.layer_ids:
            for tile_position in area[layer_id]:
                x = int(tile_position[0])
                y = int(tile_position[1])
                tile = self.level["layers"][layer_id][tile_position]
                tile_id = tile["id"]
                tileset_id = tile["tileset_id"]
                surface.blit(images[tileset_id][tile_id], (x, y))

