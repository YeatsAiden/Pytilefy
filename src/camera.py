import pygame as pg

from .settings import *

def ease_in_quart(x) -> float:
    return pg.math.clamp(x * x * x * x, 0, 1)

class Camera:
    def __init__(self, width: int, height: int) -> None:
        self.view_rect: pg.FRect = pg.FRect(0, 0, width, height)

        self.target_sprite = None
        self.target_pos = None

        self.scroll: pg.Vector2 = pg.Vector2()
        self.to_center: pg.Vector2 = pg.Vector2()
        self.scale: float = 1

    @property
    def target(self) -> pg.typing.Point:
        if self.target_sprite:
            return self.target_sprite.center
        elif self.target_pos:
            return self.target_pos
        else:
            return (DISPLAY_WIDTH//2, DISPLAY_HEIGHT//2)

    @target.setter
    def target(self, value) -> None:
        if hasattr(value, "center"):
            self.target_sprite = value
            self.target_pos = None
        elif hasattr(value, "pos"):
            self.target_sprite = None
            self.target_pos = value
        else:
            self.target_pos = (DISPLAY_WIDTH//2, DISPLAY_HEIGHT//2)

    @property
    def mouse_pos_on_display(self) -> pg.Vector2:
        mouse_x, mouse_y = pg.mouse.get_pos()
        mouse_x = (mouse_x - self.to_center[0])/self.scale
        mouse_y = (mouse_y - self.to_center[1])/self.scale
        return pg.Vector2(mouse_x, mouse_y)

    def followtarget(self, dt: float) -> None:
        self.view_rect.center = self.target
        self.scroll.x += (self.view_rect.x - self.scroll.x)
        self.scroll.y += (self.view_rect.y - self.scroll.y)

    def move(self, dt: float) -> None:
        keys_pressed = pg.key.get_pressed()
        self.target.y -= keys_pressed[pg.K_UP] * 500 * dt
        self.target.y += keys_pressed[pg.K_DOWN] * 500 * dt
        self.target.x += keys_pressed[pg.K_RIGHT] * 500 * dt
        self.target.x -= keys_pressed[pg.K_LEFT] * 500 * dt
