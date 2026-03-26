import pygame as pg
import json

from .settings import *
from .assets import images, data
from .common import *

def tuple_to_json_coord(coord: tuple[int | float, int | float]) -> str:
    return f"{round(coord[0], 3)};{round(coord[1], 3)}"

class Level(pg.sprite.Sprite):
    def __init__(self, file_path: pg.typing.FileLike) -> None:
        pg.sprite.Sprite.__init__(self)
        self.file = str(file_path) + ".json"
        self.level_data = {
            "layers": {},
            "height": 0,
            "width": 0,
        }

        # tile "type" "id" "spritesheet_id"
        # layer "is_visible" "has_collisions" "on_grid" "off_set" (later) "tiles"
        #NOTE: should add an off_set var for offset grids

        try:
            with open(self.file, "r") as f:
                self.level_data = json.load(f)
        except:
            with open(self.file, "w") as f:
                json.dump(self.level_data, f)

        # changes all the keys from
        for layer in self.level_data["layers"].values():
            layer["tiles"] = {(int(k[0]), int(k[2])): v for k, v in layer["tiles"].items()}

        self.level_rects = self.get_level_rects()
        self.on_grid_tiles = {layer_id: set(layer["tiles"]) for layer_id, layer in self.level_data["layers"].items() if layer["on_grid"]}
        self.layer_ids = sorted(list(self.level_data["layers"].keys()), key= lambda x: int(x))

    def get_tile_coordinate_at(self, point: pg.Vector2) -> pg.Vector2:
        return pg.Vector2(point.x//TILE_SIZE, point.y//TILE_SIZE)

    def greedy_horizontal_merger(self):
        rects = {}
        height = self.level_data["height"]
        width = self.level_data["width"]
        visited = {(j, i): False for i in range(height) for j in range(width)}

        for layer_id, layer in self.level_data["layers"].items():
            if not layer["has_collisions"] or not layer["on_grid"]:
                continue

            rects[layer_id] = {}

            for i in range(height):
                for j in range(width):
                    tile_pos = (j, i)
                    if visited[tile_pos] or not layer["tiles"].get(tile_pos):
                        visited[tile_pos] = True
                        continue

                    rect_width = 1
                    rect_height = 1

                    while rect_width + j < width and layer["tiles"].get((j + rect_width, i)) and not visited[(j + rect_width, i)]:
                        rect_width += 1

                    while i + rect_height < height:
                        valid = True
                        k = j
                        while k < j + rect_width:
                            if visited[(i + rect_height, k)] or not layer["tiles"].get((i + rect_height, k)):
                                valid = False
                                break
                            k += 1
                        if not valid:
                            break
                        rect_height += 1

                    for k in range(i, i + rect_height):
                        for l in range(j, j +rect_width):
                            visited[(l, k)] = True

                    # Real cursed
                    rects[layer_id].update(dict.fromkeys([(l, k) for k in range(i, i + rect_height) for l in range(j, j +rect_width)], pg.FRect(j, i, rect_width, rect_height)))

        return rects

    def get_off_grid_tiles(self):
        rects = {}

        for layer_id, layer in self.level_data["layers"]:
            if layer["on_grid"] or not layer["has_collisions"]:
                continue

            rects[layer_id] = {}

            for tile_position, tile in layer["tiles"].items():
                spritesheet_id = tile["spritesheet_id"]
                tile_id = tile["spritesheet_id"]
                tile_rect = data[spritesheet_id]["sprites"][tile_id]["rect"]
                x = round(tile_position[0], 3) + tile_rect["x"]
                y = round(tile_position[1], 3) + tile_rect["y"]
                w = tile_rect["w"]
                h = tile_rect["h"]
                rects[layer_id].update({tile_id: pg.FRect(x, y, w, h)})

        return rects

    def get_level_rects(self):
        rects = self.greedy_horizontal_merger()
        rects.update(self.get_off_grid_tiles())
        return rects

    def get_drawing_area(self, scroll: pg.Vector2):
        area = {}

        start_row = int(scroll.y // TILE_SIZE)
        end_row = int((scroll.y + DISPLAY_HEIGHT) // TILE_SIZE) + 1
        start_col = int(scroll.x // TILE_SIZE)
        end_col = int((scroll.x + DISPLAY_WIDTH) // TILE_SIZE) + 1

        positions = {(x, y) for y in range(start_row, end_row + 1) for x in range(start_col, end_col + 1)}

        camera_rect = pg.FRect(scroll.x, scroll.y, DISPLAY_WIDTH, DISPLAY_HEIGHT)

        for layer_id, layer in self.level_data["layers"].items():
            if not layer["on_grid"] and layer["is_visible"]:
                for tile_position in layer["tiles"]:
                    if scroll.x <= tile_position[0] <= scroll.x + DISPLAY_WIDTH and scroll.y <= tile_position[1] <= scroll.y + DISPLAY_HEIGHT:
                        #FIXME: make it collide with camera_rect
                        area[layer_id].add(tile_position)
            elif layer["on_grid"] and layer["is_visible"]:
                area[layer_id] = positions & self.on_grid_tiles[layer_id]

        return area

    def draw(self, surface: pg.Surface, scroll: pg.Vector2):
        #FIXME: edit to work with offgrid tiles
        area = self.get_drawing_area(scroll)
        for layer_id in self.layer_ids:
            for tile_position in area[layer_id]:
                x = int(tile_position[0])
                y = int(tile_position[1])
                tile = self.level_data["layers"][layer_id]["tiles"][tile_position]
                tile_id = tile["id"]
                tileset_id = tile["spritesheet_id"]
                surface.blit(images[tileset_id][tile_id], (x - scroll.x, y - scroll.y))

