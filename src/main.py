import pygame as pg
from pathlib import Path
import sys

from .ui import Button, Font
from .assets import load_assets, images
from .settings import *
from . import settings
from .common import *
from .editor import Editor
from .camera import Camera
from .renderer import Renderer
from .grid import Grid
from .mouse import Mouse
from .display import Display, Mover
from .entity import EntityGroup

if len(sys.argv) <= 1:
    print("What file brah >:(")
    sys.exit()

# Initial setup
pg.init()


class LevelEditor:
    def __init__(self) -> None:
        self.window = pg.display.set_mode(WINDOW_SIZE, pg.RESIZABLE)
        self.display = Display(self.window, DISPLAY_WIDTH, DISPLAY_HEIGHT)
        self.renderer = Renderer(["display", "ui"])
        self.clock = pg.time.Clock()

        load_assets()

        self.camera = Camera(0, 0, 0, 0)
        self.view_pos = Mover(0, 0)
        self.camera.target = self.view_pos
        self.level_editor = Editor(Path(sys.argv[1]), self.camera)

        self.ui_elements = EntityGroup(
            *[Button(0, 0, images["tilesets"][tileset][0], lambda:setattr(self.level_editor, "spritesheet_id", tileset)) for tileset in images["tilesets"]],
            Button(
                DISPLAY_WIDTH/2 + len(str(self.level_editor.current_layer)) * 6 + 6,
                DISPLAY_HEIGHT - 36,
                images["next_layer"],
                lambda: setattr(self.level_editor, "current_layer", self.level_editor.current_layer + 1)
                ),
            Button(
                DISPLAY_WIDTH/2 - len(str(self.level_editor.current_layer)) * 6 - 38,
                DISPLAY_HEIGHT - 36,
                images["prev_layer"],
                lambda: setattr(self.level_editor, "current_layer", self.level_editor.current_layer + 1)
                )
        )
        self.mouse = Mouse(self.ui_elements)

        self.grid = Grid(self.camera)
        self.group = EntityGroup(self.grid, self.display, self.level_editor.level)

        self.smol_font = Font(images["smol_font"], [1, 2, 3], 1)

        self.frame_time: float = 0;
        self.done = False

    def run(self) -> None:
        while not self.done:
            self.window.fill("black")

            self.level_editor.place_tile()
            self.level_editor.delete_tile()
            self.smol_font.blit("display", str(self.level_editor.current_layer), DISPLAY_WIDTH/2 - len(str(self.level_editor.current_layer)) * 6, 360, 1, 2, 1)
            self.smol_font.blit("display", f"type: {self.level_editor.tile_type}".lower(), 4, 350, 1, 2, 1)
            self.smol_font.blit("display", f"visible: {self.level_editor.is_visible}".lower(), 4, 360, 1, 2, 1)
            self.smol_font.blit("display", f"collision: {self.level_editor.has_collisions}".lower(), 4, 370, 1, 2, 1)

            self.event_loop()

            self.view_pos.move(self.frame_time)
            self.grid.update()
            self.mouse.update()
            self.display.update()
            self.camera.follow_target(self.frame_time)
            self.ui_elements.update()

            self.group.blit()
            self.ui_elements.blit()
            self.renderer.render({"display": self.display.image, "ui": self.display.image, "window": self.window})
            self.renderer.clear()

            pg.display.update()

            self.frame_time = self.clock.tick(FPS) / 1000

    def event_loop(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.level_editor.save_level()
                self.done = True
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_F11:
                    settings.FULL_SCREEN = not settings.FULL_SCREEN
                    pg.display.set_mode((0, 0), pg.RESIZABLE | pg.FULLSCREEN) if settings.FULL_SCREEN else pg.display.set_mode(WINDOW_SIZE, pg.RESIZABLE)

