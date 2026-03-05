import pygame as pg


images = {}

props = load_images(PATHS["objects"])
spawns = load_images(PATHS["spawns"])
tile_sets = {file.split('.')[0]: make_tileset_dict(PATHS['tilesets'] + "/" + file) for file in get_file_names(PATHS['tilesets']) if file.split('.')[1] == "png"}
tile_sets_rules = {file.split('.')[0]: load_json(PATHS['tilesets'] + "/" + file) for file in get_file_names(PATHS['tilesets']) if file.split('.')[1] == "json"}
smol_font = Font(PATHS["fonts"] + "/" + "smol_font.png", [1, 2, 3], 1)
new_layer = Button(PATHS["buttons"] + "/" + "new_layer.png", DISPLAY_WIDTH - 36, 4)
next_layer = Button(PATHS["buttons"] + "/" + "next_layer.png")
prev_layer = Button(PATHS["buttons"] + "/" + "prev_layer.png")
cursor_image = pg.image.load(PATHS["cursors"] + "/" + "cursor.png").convert_alpha()
