import pygame as pg

from .settings import *

def ease_in_quart(x) -> float:
    return pg.math.clamp(x * x * x * x, 0, 1)

class Camera(pg.sprite.LayeredUpdates):
    def __init__(self, x: float, y: float, width: int, height: int) -> None:
        super().__init__(self);
        self.display: pg.Surface = pg.Surface(DISPLAY_SIZE)
        self.frame: pg.Surface = pg.Surface(DISPLAY_SIZE)

        self._view_rect: pg.FRect = pg.FRect(x, y, width, height)
        self._target: pg.Vector2 = pg.Vector2()

        self.scroll: pg.Vector2 = pg.Vector2()
        self.to_center: pg.Vector2 = pg.Vector2()
        self.scale: float = 1

    @property
    def target(self) -> pg.Vector2:
        return self._target

    @target.setter
    def target(self, value: pg.typing.Point) -> None:
        self._target = pg.Vector2(value)

    @property
    def pos(self) -> pg.Vector2:
        return pg.Vector2(self._view_rect.topleft)

    @target.setter
    def pos(self, value: pg.typing.Point) -> None:
        self._view_rect = value

    @property
    def mouse_pos_display(self) -> pg.Vector2:
        mouse_x, mouse_y = pg.mouse.get_pos()
        mouse_x = (mouse_x - self.to_center[0])/self.scale
        mouse_y = (mouse_y - self.to_center[1])/self.scale
        return pg.Vector2(mouse_x, mouse_y)

    def follow_target(self, dt: float) -> None:
        self._view_rect.center = self.target
        self.scroll.x += (self._view_rect.centerx - self.scroll.x)/5
        self.scroll.y += (self._view_rect.centery - self.scroll.y)/5

    def render_sprites(self, dt: float) -> None:
        self.follow_target(dt)
        layers = self.layers()
        for layer in layers:
            for sprite in self.get_sprites_from_layer(layer):
                sprite.draw(self.display, -self.scroll)

    def resize_display(self, window :pg.Surface) -> None:
        self.scale = min(window.get_width() / self.display.get_width(), window.get_height() / self.display.get_height())
        self.frame = pg.transform.scale_by(self.display, self.scale)
        self.xy_change = [(window.get_width() - self.frame.get_width()) // 2, (window.get_height() - self.frame.get_height()) // 2]

    def render_display(self, window: pg.Surface, dt: float) -> None:
        self.display.fill("black")
        self.render_sprites(dt)
        self.resize_display(window)
        window.blit(self.frame, self.to_center)

    def move(self, dt: float) -> None:
        keys_pressed = pg.key.get_pressed()
        self._view_rect.y -= keys_pressed[pg.K_UP] * 5
        self._view_rect.y += keys_pressed[pg.K_DOWN] * 5
        self._view_rect.x += keys_pressed[pg.K_RIGHT] * 5
        self._view_rect.x -= keys_pressed[pg.K_LEFT] * 5

