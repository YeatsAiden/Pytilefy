import pygame as pg
from pathlib import Path
import time, sys

from .assets import load_assets, images, data
from .settings import *
from .common import *
from .ui import Button, Font
from .editor import Editor
from .camera import Camera
from .renderer import Renderer
from .grid import Grid
from .mouse import Mouse
from .display import Display
from .entity_group import EntityGroup

if len(sys.argv) <= 1:
    print("What file brah >:(")
    sys.exit()

# Initial setup
pg.init()

class LevelEditor:
    def __init__(self) -> None:
        self.window = pg.display.set_mode(WINDOW_SIZE, pg.RESIZABLE)
        self.display = Display(self.window, DISPLAY_WIDTH, DISPLAY_HEIGHT)
        self.clock = pg.time.Clock()
        pg.mouse.set_visible(MOUSE_VISIBLE)

        self.FULL_SCREEN = False

        load_assets()

        self.renderer = Renderer(["display", "ui"])
        self.camera = Camera(DISPLAY_WIDTH, DISPLAY_HEIGHT)
        self.camera_pos = pg.Vector2()
        self.camera.target = self.camera_pos

        self.level_editor = Editor(Path(sys.argv[1]))

        self.grid = Grid(self.camera)
        self.mouse = Mouse()

        self.group = EntityGroup(self.grid, self.mouse, self.display)

        # smol_font = Font(PATHS["fonts"] + "/" + "smol_font.png", [1, 2, 3], 1)
        # new_layer = Button(PATHS["buttons"] + "/" + "new_layer.png", DISPLAY_WIDTH - 36, 4)
        # next_layer = Button(PATHS["buttons"] + "/" + "next_layer.png")
        # prev_layer = Button(PATHS["buttons"] + "/" + "prev_layer.png")

        self.frame_time: float = 0;

    def run(self) -> None:
        while True:
            self.window.fill("black")
            keys_pressed = pg.key.get_pressed()
            mouse_pressed = pg.mouse.get_pressed()

            current_time = time.time()

            self.level_editor.place_tile(self.camera)
            # draw level
            # self.level_editor.draw_level(display, cam_pos)

            # smol_font.draw_text(display, str(level_editor.current_layer), DISPLAY_WIDTH/2 - len(str(level_editor.current_layer)) * 6, 360, 1, 3)
            # smol_font.draw_text(display, f"type: {level_editor.image_type[level_editor.type_id]}".lower(), 4, 350, 1, 2)
            # smol_font.draw_text(display, f"visible: {level_editor.visible}".lower(), 4, 360, 1, 2)
            # smol_font.draw_text(display, f"collision: {level_editor.collision}".lower(), 4, 370, 1, 2)

            self.event_loop()

            self.grid.update()
            self.mouse.update()
            self.display.update()

            self.group.blit(self.renderer)

            self.renderer.render({"display": self.display.image, "window": self.window})
            self.renderer.clear()

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

