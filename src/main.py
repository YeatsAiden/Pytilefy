import pygame as pg
import time, sys

from .settings import *
from .common import *
from .ui import Button, Font
from .editor import Editor
from .camera import Camera
from .grid import Grid

if len(sys.argv) <= 1:
    print("What file brah >:(")
    sys.exit()

# Initial setup
pg.init()

class LevelEditor:
    def __init__(self) -> None:
        self.window = pg.display.set_mode(WINDOW_SIZE, pg.RESIZABLE)
        self.clock = pg.time.Clock()
        pg.mouse.set_visible(MOUSE_VISIBLE)

        self.FULL_SCREEN = False

        self.camera = Camera(-self.window.get_width()/2, -self.window.get_height()/2, DISPLAY_WIDTH, DISPLAY_HEIGHT)
        self.camera.target = self.camera.pos
        self.level_editor = Editor(sys.argv[1])
        self.grid = Grid()
        # smol_font = Font(PATHS["fonts"] + "/" + "smol_font.png", [1, 2, 3], 1)
        # new_layer = Button(PATHS["buttons"] + "/" + "new_layer.png", DISPLAY_WIDTH - 36, 4)
        # next_layer = Button(PATHS["buttons"] + "/" + "next_layer.png")
        # prev_layer = Button(PATHS["buttons"] + "/" + "prev_layer.png")
        self.camera.add(self.grid)

        self.frame_time: float = 0;

    def run(self) -> None:
        while True:
            self.window.fill("black")
            keys_pressed = pg.key.get_pressed()
            mouse_pressed = pg.mouse.get_pressed()

            current_time = time.time()

            # draw level
            # self.level_editor.draw_level(display, cam_pos)

            # smol_font.draw_text(display, str(level_editor.current_layer), DISPLAY_WIDTH/2 - len(str(level_editor.current_layer)) * 6, 360, 1, 3)
            # smol_font.draw_text(display, f"type: {level_editor.image_type[level_editor.type_id]}".lower(), 4, 350, 1, 2)
            # smol_font.draw_text(display, f"visible: {level_editor.visible}".lower(), 4, 360, 1, 2)
            # smol_font.draw_text(display, f"collision: {level_editor.collision}".lower(), 4, 370, 1, 2)
            self.event_loop()

            self.grid.update(self.camera)
            self.camera.zoom_in(self.frame_time)
            self.camera.move(self.frame_time)

            # Resizing display to window size
            self.camera.follow_target(self.frame_time)
            self.camera.render_display(self.window, self.frame_time)
            pg.display.update()

            self.frame_time = self.clock.tick(FPS) / 1000

    def event_loop(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_F11:
                    self.FULL_SCREEN = not self.FULL_SCREEN
                    pg.display.set_mode((0, 0), pg.RESIZABLE | pg.FULLSCREEN) if self.FULL_SCREEN else pg.display.set_mode(WINDOW_SIZE, pg.RESIZABLE)
