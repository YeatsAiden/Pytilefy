import pygame as pg
import json

from .settings import *
from .assets import images, data
from .common import *
from .entity import Entity

def tuple_to_json_coord(coord: tuple[int, int]) -> str:
    return f"{coord[0]};{coord[1]}"

def json_to_tuple_coord(coord: str) -> tuple[int, int]:
    x, y = map(int, coord.split(";"))
    return (x, y)

class Level(Entity):
    def __init__(self, file_path: pg.typing.FileLike) -> None:
        super().__init__()
        self.file = str(file_path)
        self.level_data = {
            "start_position": [0, 0], # Top and left most tile coordinate
            "height": 0, # Height of world in tiles
            "width": 0, # Width of world in tiles
            "layers": {},
        }

        # Layer anatomy
        # z: {
        #     "chunks": {chunks},
        #     "is_visible": True,
        #     "has_collisions": True,
        # }

        # Tile anatomy
        # (x, y): "type" "id" "spritesheet_id" "off_set" (for tiles that don't exactly fit the grid)

        # Chunk anatomy
        # (x, y): {
        #     "on_grid_tiles": {
        #         # Chunks with on grid tiles in them.
        #         },
        #     "off_grid_tiles": {
        #         # Chunks with off grid tiles in them.
        #         }
        #     }

        try:
            with open(self.file, "r") as f:
                self.level_data = json.load(f)
        except:
            print(f"Level {self.file} doesn't exist")
            self.level_data["tile_size"] = TILE_SIZE
            self.level_data["chunk_size"] = CHUNK_SIZE


        # changes all the keys from strings to tuples
        for layer in self.level_data["layers"].values():
            layer["chunks"] = {json_to_tuple_coord(chunk_coord): chunk for chunk_coord, chunk in layer["chunks"].items()}
            for chunk_coord in layer["chunks"]:
                layer["chunks"][chunk_coord]["on_grid_tiles"] = {json_to_tuple_coord(tile_coord): tile for tile_coord, tile in layer["chunks"][chunk_coord]["on_grid_tiles"].items()}
                layer["chunks"][chunk_coord]["off_grid_tiles"] = {json_to_tuple_coord(tile_coord): tile for tile_coord, tile in layer["chunks"][chunk_coord]["off_grid_tiles"].items()}

        self.level_rects = self.get_level_rects()
        # self.on_grid_tiles = {layer_id: set(layer["tiles"]) for layer_id, layer
        #                       in self.level_data["layers"].items() if
        #                       layer["on_grid"]}
        #
        # self.layer_ids = sorted(list(self.level_data["layers"].keys()), key= lambda x: int(x))

        self.target = "display"

    def get_tile_pos_at(self, point: pg.typing.Point) -> tuple[int, int]:
        return (point[0]//self.level_data["tile_size"][0], point[1]//self.level_data["tile_size"][1])

    def get_chunk_pos_at(self, point: pg.typing.Point) -> tuple[int, int]:
        chunk_size = self.level_data["chunk_size"]
        x, y = point[0]//chunk_size * chunk_size, point[1]//chunk_size * chunk_size
        x += -1 if point[0] < x else 0
        y += -1 if point[1] < y else 0
        return (x, y)

    def greedy_horizontal_merger(self):
        rects = {}
        #FIXME: get rid of this var
        chunk_size = self.level_data["chunk_size"]
        start_x, start_y = self.level_data["start_position"]
        end_x, end_y = start_x + self.level_data["width"], start_y + self.level_data["height"]

        visited = {(j, i): False for i in range(start_y, end_y) for j in range(start_x, end_x)}

        for layer_id, layer in self.level_data["layers"].items():
            if not layer["has_collisions"]:
                continue

            rects[layer_id] = {}

            for i in range(start_y, end_y):
                for j in range(start_x, end_x):
                    tile_pos = (j, i)
                    chunk_pos = self.get_chunk_pos_at(tile_pos)

                    chunk = layer["chunks"].get(chunk_pos)
                    if not chunk:
                        visited[tile_pos] = True
                        continue
                    tile = chunk["on_grid_tiles"].get(tile_pos)

                    if visited[tile_pos] or not (chunk and tile):
                        visited[tile_pos] = True
                        continue

                    rect_width = 1
                    rect_height = 1

                    next_tile_pos = (j + rect_width, i)
                    next_chunk_pos = self.get_chunk_pos_at(next_tile_pos)

                    next_chunk = layer["chunks"].get(next_chunk_pos)
                    next_tile = next_chunk["on_grid_tiles"].get(next_tile_pos)

                    while rect_width + j < end_x and next_chunk and next_tile and not visited[(j + rect_width, i)]:
                        rect_width += 1

                    while i + rect_height < end_y:
                        valid = True
                        k = j
                        while k < j + rect_width:
                            next_tile_pos = (i + rect_height, k)
                            next_chunk_pos = self.get_chunk_pos_at(next_tile)

                            next_chunk = layer["chunks"].get(next_chunk_pos)
                            next_tile = next_chunk["on_grid_tiles"].get(next_tile_pos)

                            if visited[(i + rect_height, k)] or not (next_chunk and next_tile):
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
                    rect = pg.FRect(j, i, rect_width, rect_height)
                    rects[layer_id].update(
                            dict.fromkeys(
                                [(l, k) for k in range(i, i + rect_height) for l in range(j, j + rect_width)], rect
                                )
                            )

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
        #FIXME: make work with width and height tile size
        area = {}

        start_row = int(scroll.y // self.level_data["tile_size"])
        end_row = int((scroll.y + DISPLAY_HEIGHT) // self.level_data["tile_size"]) + 1
        start_col = int(scroll.x // self.level_data["tile_size"])
        end_col = int((scroll.x + DISPLAY_WIDTH) // self.level_data["tile_size"]) + 1

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

