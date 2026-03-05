from .settings import *
from .common import *
from .core_funcs import *
from .ui import *


class Editor:
    def __init__(self, file_path: pg.typing.FileLike) -> None:
        self.level = {}
        if file_path:
            with open(file_path, "w") as f:
                self.level = json.load(f)

    def place_tile(self, tile_pos_key: str):
        self.levels[self.current_level][str(self.current_layer)][tile_pos_key] = {
            "type": self.image_type[self.type_id],
            "collision": self.collision,
            "visible": self.visible,
        }

        image_type = self.image_type[self.type_id]

        if image_type == "tiles":
            self.levels[self.current_level][str(self.current_layer)][tile_pos_key].update({
                "tile_set": self.current_item,
                "id": self.tile_set_rules[self.current_item]["tile_id"]
            })
        else:
            self.levels[self.current_level][str(self.current_layer)][tile_pos_key].update({
                "id": self.current_item
            })

        self.auto_tile()


    def delete_tile(self, tile_pos_key: str):
        self.levels[self.current_level][str(self.current_layer)].pop(tile_pos_key)
        self.auto_tile()

    
    def add_new_layer(self):
        self.levels[self.current_level][str(len(self.levels[self.current_level]))] = {}
    

    def save_level(self):
        self.auto_tile()
        with open(PATHS["levels"] + "/" + f"{self.current_level}.json", "w") as f: 
            json.dump(self.levels[self.current_level], f)


    def auto_tile(self):
        for layer in self.levels[self.current_level]:
            for tile in self.levels[self.current_level][layer]:
                if self.levels[self.current_level][layer][tile]["type"] == "tiles":
                    x, y = map(int, tile.split(":"))
                    code = ""

                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            if f"{x + j}:{y + i}" in self.levels[self.current_level][layer]:
                                code += "1" if self.levels[self.current_level][layer][f"{x + j}:{y + i}"]["type"] == "tiles" else "0"
                            else:
                                code += "0"
                    tile_set = self.levels[self.current_level][layer][tile]["tile_set"]
                    if code in self.tile_set_rules[tile_set]:
                        self.levels[self.current_level][layer][tile]["id"] = self.tile_set_rules[tile_set][code]


    def get_area(self, cam_pos: pg.Vector2):
        area = {}

        start_row = int(cam_pos[1] // TILE_SIZE)
        end_row = int((cam_pos[1] + DISPLAY_HEIGHT) // TILE_SIZE) + 1
        start_col = int(cam_pos[0] // TILE_SIZE)
        end_col = int((cam_pos[0] + DISPLAY_WIDTH) // TILE_SIZE) + 1

        positions = {f"{x}:{y}" for y in range(start_row, end_row + 1) for x in range(start_col, end_col + 1)}

        for layer in self.levels[self.current_level]:
            area[layer] = positions & set(self.levels[self.current_level][layer])

        return area

    def draw_level(self, surf: pg.Surface, positions: dict, cam_pos: pg.Vector2):
        for layer in positions:
            for tile in positions[layer]:
                x, y = map(int, tile.split(":"))
                tile_type = self.levels[self.current_level][layer][tile]["type"]
                tile_id = self.levels[self.current_level][layer][tile]["id"]
                if tile_type == "tiles":
                    tile_set = self.levels[self.current_level][layer][tile]["tile_set"]
                    surf.blit(self.types[tile_type][tile_set][tile_id], (x * TILE_SIZE - cam_pos.x, y * TILE_SIZE - cam_pos.y))
                else:
                    surf.blit(self.types[tile_type][tile_id], (x * TILE_SIZE - cam_pos.x, y * TILE_SIZE - cam_pos.y))
