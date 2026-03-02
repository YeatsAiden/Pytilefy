import pygame as pg
import time, sys

from .consts import *
from .core_funcs import *
from .ui import Button, Font
from .level import Level
from .editor import Editor
from .camera import Camera

# Initial setup
pg.init()

window = pg.display.set_mode(WINDOW_SIZE, pg.RESIZABLE)
display = pg.Surface(DISPLAY_SIZE)
clock = pg.time.Clock()

pg.mouse.set_visible(MOUSE_VISIBLE)

camera = Camera(0, 0, 1, 1)

# Loading assets
objects = load_images(PATHS["objects"])
spawns = load_images(PATHS["spawns"])
tile_sets = {file.split('.')[0]: make_tileset_dict(PATHS['tilesets'] + "/" + file) for file in get_file_names(PATHS['tilesets']) if file.split('.')[1] == "png"}
tile_sets_rules = {file.split('.')[0]: load_json(PATHS['tilesets'] + "/" + file) for file in get_file_names(PATHS['tilesets']) if file.split('.')[1] == "json"}

smol_font = Font(PATHS["fonts"] + "/" + "smol_font.png", [1, 2, 3], 1)
new_layer = Button(PATHS["buttons"] + "/" + "new_layer.png", DISPLAY_WIDTH - 36, 4)
next_layer = Button(PATHS["buttons"] + "/" + "next_layer.png")
prev_layer = Button(PATHS["buttons"] + "/" + "prev_layer.png")

cursor_image = pg.image.load(PATHS["cursors"] + "/" + "cursor.png").convert_alpha()

# Class initialization
level_editor = Editor(objects, spawns, tile_sets, tile_sets_rules, TILE_SIZE)

# Display stuff
window_pos = pg.Vector2(-window.get_width()/2, -window.get_height()/2)
cam_pos = pg.Vector2(0, 0)
xy_change = [0, 0]
scale = 1
camera.target = cam_pos
# Game loop
while True:
    display.fill("black")

    keys_pressed = pg.key.get_pressed()
    mouse_pressed = pg.mouse.get_pressed()

    current_time = time.time()

    cam_pos.x += (window_pos.x - cam_pos.x)/5
    cam_pos.y += (window_pos.y - cam_pos.y)/5

    mouse_x, mouse_y = pg.mouse.get_pos()
    mouse_x = (mouse_x - xy_change[0])/scale
    mouse_y = (mouse_y - xy_change[1])/scale

    window_pos.y -= keys_pressed[pg.K_UP] * 5
    window_pos.y += keys_pressed[pg.K_DOWN] * 5
    window_pos.x += keys_pressed[pg.K_RIGHT] * 5
    window_pos.x -= keys_pressed[pg.K_LEFT] * 5

    tile_pos_key = f"{int((mouse_x + window_pos.x)//TILE_SIZE)}:{int((mouse_y + window_pos.y)//TILE_SIZE)}"

    if new_layer.check_click([mouse_x, mouse_y], mouse_pressed, current_time):
        level_editor.add_new_layer()

    if next_layer.check_click([mouse_x, mouse_y], mouse_pressed, current_time):
        level_editor.current_layer += 1

    if prev_layer.check_click([mouse_x, mouse_y], mouse_pressed, current_time):
        level_editor.current_layer -= 1

    elif mouse_pressed[0]:
        level_editor.place_tile(tile_pos_key)
    elif mouse_pressed[2] and tile_pos_key in level_editor.levels[level_editor.current_level][str(level_editor.current_layer)]:
        level_editor.delete_tile(tile_pos_key)

    level_editor.current_layer = max(0, min(len(level_editor.levels[level_editor.current_level]) - 1, level_editor.current_layer))

    # Draw grid

    # draw level
    area = level_editor.get_area(cam_pos)
    level_editor.draw_level(display, area, cam_pos)

    # draw buttons
    prev_layer.set_position(DISPLAY_WIDTH/2 - len(str(level_editor.current_layer)) * 6 - 38, DISPLAY_HEIGHT - 36)
    prev_layer.draw(display)

    next_layer.set_position(DISPLAY_WIDTH/2 + len(str(level_editor.current_layer)) * 6 + 6, DISPLAY_HEIGHT - 36)
    next_layer.draw(display)

    new_layer.draw(display)

    for button_id in level_editor.buttons[level_editor.image_type[level_editor.type_id]]:
        button = level_editor.buttons[level_editor.image_type[level_editor.type_id]][button_id]
        button.draw(display)
        if button.check_click([mouse_x, mouse_y], mouse_pressed, current_time):
            level_editor.current_item = button.id

    smol_font.draw_text(display, str(level_editor.current_layer), DISPLAY_WIDTH/2 - len(str(level_editor.current_layer)) * 6, 360, 1, 3)
    smol_font.draw_text(display, f"type: {level_editor.image_type[level_editor.type_id]}".lower(), 4, 350, 1, 2)
    smol_font.draw_text(display, f"visible: {level_editor.visible}".lower(), 4, 360, 1, 2)
    smol_font.draw_text(display, f"collision: {level_editor.collision}".lower(), 4, 370, 1, 2)

    # draw cursor
    display.blit(cursor_image, [mouse_x, mouse_y])

    # event_loop
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_F11:
                FULL_SCREEN = not FULL_SCREEN
                pg.display.set_mode((0, 0), FLAGS | pg.FULLSCREEN) if FULL_SCREEN else pg.display.set_mode(WINDOW_SIZE, FLAGS)

            if event.key == pg.K_n:
                level_editor.add_new_layer()

            if event.key == pg.K_s:
                level_editor.save_level()

            if event.key == pg.K_c:
                level_editor.toggle_collision()

            if event.key == pg.K_v:
                level_editor.toggle_visible()

            if event.key == pg.K_d:
                level_editor.current_layer += 1
            if event.key == pg.K_a:
                level_editor.current_layer -= 1

            if event.key == pg.K_e:
                level_editor.type_id += 1
                level_editor.type_id = max(0, min(len(level_editor.image_type) - 1, level_editor.type_id))  
                level_editor.current_item = list(level_editor.types[level_editor.image_type[level_editor.type_id]])[0]
            if event.key == pg.K_q:
                level_editor.type_id -= 1
                level_editor.type_id = max(0, min(len(level_editor.image_type) - 1, level_editor.type_id))  
                level_editor.current_item = list(level_editor.types[level_editor.image_type[level_editor.type_id]])[0]
  
    # Resizing display to window size
    display_cp, xy_change, scale = resize_surface(window, display)
    window.blit(display_cp, xy_change)

    pg.display.update()
    dt = clock.tick(FPS) / 1000
