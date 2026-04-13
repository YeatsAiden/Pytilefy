import pygame as pg
import json

from .settings import *
from .assets import images, data
from .common import *
from .renderer import Renderer
from .entity import Entity
from .camera import Camera

def tuple_to_json_pos(coord: tuple[int, int]) -> str:
    return f"{coord[0]};{coord[1]}"

def json_to_tuple_pos(coord: str) -> tuple[int, int]:
    x, y = map(int, coord.split(";"))
    return (x, y)

def convert_pos_to(level_data, convert):
    for layer_id in list(level_data["layers"]):
        level_data["layers"][int(layer_id)] = level_data["layers"].pop(layer_id)

    for layer in level_data["layers"].values():
        layer["chunks"] = {convert(chunk_coord): chunk for chunk_coord, chunk in layer["chunks"].items()}
        for chunk_coord in layer["chunks"]:
            layer["chunks"][chunk_coord] = {convert(tile_coord): tile for tile_coord, tile in layer["chunks"][chunk_coord].items()}


class Level(Entity):
    def __init__(self, file_path: pg.typing.FileLike, camera: Camera) -> None:
        super().__init__()
        self.file = str(file_path)
        self.camera = camera

        self.data = {
            "start_pos": [0, 0], # Top and left most tile coordinate
            "size": [0, 0], # Height of world in tiles
            "layers": {},
        }

        # Layer anatomy


        # Tile anatomy
        # (x, y): "type" "id" "spritesheet_id" "off_set" (for tiles that don't exactly fit the grid)

        # Chunk anatomy
        # (x, y): {
        #       tiles (off grid and on grid)
        #     }
        # off grid

        try:
            with open(self.file, "r") as f:
                self.data = json.load(f)
        except:
            print(f"Level {self.file} doesn't exist")
            self.data["tile_size"] = TILE_SIZE
            self.data["chunk_size"] = CHUNK_SIZE

        convert_pos_to(self.data, json_to_tuple_pos)

        self.target = "display"

    def get_tile_pos_at(self, x, y) -> tuple[int, int]:
        tile_size = self.data["tile_size"]
        return int(x//tile_size[0]), int(y//tile_size[1])

    def get_chunk_pos_at(self, x, y) -> tuple[int, int]:
        chunk_size = self.data["chunk_size"]
        return int(x//chunk_size), int(y//chunk_size)

    @property
    def drawing_area(self):
        area = {}

        start_pos = self.get_chunk_pos_at(*self.get_tile_pos_at(*self.camera.bound_rect.topleft))
        end_pos = self.get_chunk_pos_at(*self.get_tile_pos_at(self.camera.bound_rect.x + DISPLAY_WIDTH, self.camera.bound_rect.y + DISPLAY_HEIGHT))

        positions = {(x, y) for y in range(start_pos[1], end_pos[1] + 1) for x in range(start_pos[0], end_pos[0] + 1)}

        for layer_id, layer in self.data["layers"].items():
            if layer["is_visible"] == True:
               area[layer_id] = positions & layer["chunks"].keys()

        return area

    def blit(self) -> None:
        tile_size = self.data["tile_size"]
        for layer_id, layer in self.drawing_area.items():
            for chunk_id in layer:
                for tile_pos, tile in self.data["layers"][layer_id]["chunks"][chunk_id].items():
                    image = images["tilesets"][tile["spritesheet_id"]][tile["id"]]
                    self.objects["Renderer"].blit(int(layer_id), self.target, image, (tile_pos[0] * tile_size[0] - self.camera.scroll[0], tile_pos[1] * tile_size[1] - self.camera.scroll[1]))

