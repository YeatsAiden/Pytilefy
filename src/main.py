import pygame as pg
import time, sys

from .settings import *
from .common import *
from .core_funcs import *
from .ui import Button, Font
from .editor import Editor
from .camera import Camera
from .grid import Grid

# Initial setup
pg.init()

FULL_SCREEN = False

class LevelEditor:
    def __init__(self) -> None:
        self.window = pg.display.set_mode(WINDOW_SIZE, pg.RESIZABLE)
        self.camera = Camera(-self.window.get_width()/2, -self.window.get_height()/2, DISPLAY_WIDTH, DISPLAY_HEIGHT)
        clock = pg.time.Clock()
        pg.mouse.set_visible(MOUSE_VISIBLE)

        self.level_editor = Editor(ASSETS_DIRECTORY / "levels")
        self.grid = Grid()

        while True:
            keys_pressed = pg.key.get_pressed()
            mouse_pressed = pg.mouse.get_pressed()

            current_time = time.time()
            tile_pos_key = f"{}:{}"

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

            # event_loop
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_F11:
                        FULL_SCREEN = not FULL_SCREEN
                        pg.display.set_mode((0, 0), pg.RESIZABLE | pg.FULLSCREEN) if FULL_SCREEN else pg.display.set_mode(WINDOW_SIZE, pg.RESIZABLE)

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
            self.camera.follow_target()
            self.camera.render_display(self.window, dt)
            pg.display.update()
            frame_time = clock.tick(FPS) / 1000

