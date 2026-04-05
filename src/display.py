import pygame as pg

from .renderer import Renderer
from .entity import Entity


class Mover(Entity):
    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self.pos.update(x, y)

    def move(self, dt: float) -> None:
        keys_pressed = pg.key.get_pressed()
        self.pos.y -= keys_pressed[pg.K_UP] * 500 * dt
        self.pos.y += keys_pressed[pg.K_DOWN] * 500 * dt
        self.pos.x += keys_pressed[pg.K_RIGHT] * 500 * dt
        self.pos.x -= keys_pressed[pg.K_LEFT] * 500 * dt


class Display(Entity):
    def __init__(self, window: pg.Surface, width: int, height: int, **kwargs) -> None:
        super().__init__()
        self.window = window
        self.image = pg.Surface((width, height), kwargs["flags"] if "flags" in kwargs else 0)
        self.scale: float = min(self.window.width/self.image.width, self.window.height/self.image.height)
        self.frame: pg.Surface
        self.z = -1

    @property
    def mouse_pos_on_display(self) -> tuple[float, float]:
        mouse_x, mouse_y = pg.mouse.get_pos()
        mouse_x = (mouse_x - self.pos.x)/self.scale
        mouse_y = (mouse_y - self.pos.y)/self.scale
        return mouse_x, mouse_y

    def update(self, *args, **kwargs) -> None:
        # scales up the display up to the window size.
        self.scale = min(self.window.get_width() / self.image.get_width(), self.window.get_height() / self.image.get_height())
        self.frame = pg.transform.scale_by(self.image, self.scale)
        self.pos.x, self.pos.y = (self.window.get_width() - self.frame.get_width()) // 2, (self.window.get_height() - self.frame.get_height()) // 2

    def blit(self, renderer: Renderer) -> None:
        renderer.blit(self.z, self.target, self.frame, self.pos)

