from .consts import *
from .core_funcs import *
from .ui import *


class Editor:
    def __init__(self, objects: dict, spawns: dict, tile_sets: dict, tile_set_rules: dict, tile_size: int, level_path: str = None) -> None:
        self.tile_size = tile_size

        self.types = {
            "tiles": tile_sets,
            "objects": objects,
            "spawns": spawns,
        }
        self.image_type = list(self.types)
        self.type_id = 0

        self.current_item = list(self.types[self.image_type[self.type_id]])[0]

        self.tile_set_rules = tile_set_rules

        self.levels = {}
        self.current_level = str(len(get_file_names(PATHS['levels'])))
        self.current_layer = 0

        self.collision = True
        self.visible = True

        self.buttons = {}
        for image_type in self.image_type:
            if image_type == "tiles":
                self.buttons["tiles"] = {}
                for i, tile_set in enumerate(self.types[image_type]):
                    self.buttons["tiles"][tile_set] = Button(self.types[image_type][tile_set][27], 4 + i * TILE_SIZE, 4)
                    self.buttons["tiles"][tile_set].id = tile_set
            else:
                self.buttons[image_type] = {}
                for i, image in enumerate(self.types[image_type]):
                    self.buttons[image_type][image] = Button(self.types[image_type][image], 4 * i + i * TILE_SIZE, 4)
                    self.buttons[image_type][image].id = image
                    
        
        if get_file_names(PATHS['levels']):
            if level_path == None:
                for path in get_file_names(PATHS['levels']):
                    level_name, level_data = path.split(".")[0], load_json(PATHS['levels'] + '/' + path)
                    self.current_level = level_name
                    self.levels[level_name] = level_data
            else:
                level_name, level_data = level_path.split(".")[0], load_json(level_path)
                self.current_level = level_name
                self.levels[level_name] = level_data
        else:
            self.current_level = len(get_file_names(PATHS['levels']))
            self.levels[self.current_level] = {
                "0": {},
            }
    

    def toggle_visible(self):
        self.visible = not self.visible


    def toggle_collision(self):
        self.collision = not self.collision


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
