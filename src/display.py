import pygame as pg

from .entity import Entity
from .settings import DISPLAY_RATIO


class Display(Entity):
    def __init__(self, window: pg.Surface, width: int, height: int, **kwargs) -> None:
        super().__init__()
        self.window = window
        self.image = pg.Surface((width, height), kwargs["flags"] if "flags" in kwargs else 0)
        self.scale: float = DISPLAY_RATIO
        self.frame: pg.Surface

    def update(self, *args, **kwargs) -> None:
        # scales up the display up to the window size.
        self.scale = min(self.window.get_width() / self.image.get_width(), self.window.get_height() / self.image.get_height())
        self.frame = pg.transform.scale_by(self.image, self.scale)
        self.pos.x, self.pos.y = (self.window.get_width() - self.frame.get_width()) // 2, (self.window.get_height() - self.frame.get_height()) // 2

