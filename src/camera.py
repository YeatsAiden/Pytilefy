import pygame as pg

def ease_in_quart(x) -> int:
    return pg.math.constrain(x * x * x * x, 0, 1)

class Camera(pg.sprite.LayeredUpdates):
    def __init__(self, x, y, w, h) -> None:
        super().__init__(self);
        self._target: pg.Vector2 = None
        self._view_rect = pg.FRect(x, y, w, h)
        self.cam_pos: pg.Vector2 = pg.Vector2()

    @property
    def target(self) -> pg.Vector2:
        return self._target

    @target.setter
    def target(self, value: pg.typing.Point):
        self._target = pg.Vector2(value)

    def follow_target(self, dt: float):
        self.view_rect.center = self.target
        self.cam_pos = self.target - pg.Vector(self.view_rect)

    def draw(self, surface: pg.Surface, dt: float):
        follow_target(dt)
        layers = self.layers()
        for layer in layers:
            for sprite in self.get_sprites_from_layer():
                sprite.draw(surface, -self.cam_pos)


