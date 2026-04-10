import pygame as pg
from collections.abc import Callable # For Typing duhhhhhhh

from .settings import *
from .assets import clip_img
from .entity import Entity
from .objects import Object


# You will never find out where I got the func parameter idea from (Thx mattiss)
class Button(Entity):
    def __init__(self, x, y, image: pg.Surface, func: Callable = lambda : None ) -> None:
        super().__init__()
        self.pos.update(x, y)
        self.image = image
        self.size = self.image.size
        self.func = func

        self.click_cooldown = 1
        self.time_since_click = 0

        self.target = "ui"

    def update(self, *args, **kwargs) -> None:
        mouse_pos = self.objects["Mouse"].display_pos
        mouse_pressed = pg.mouse.get_pressed()

        if self.rect.collidepoint(mouse_pos) and mouse_pressed[0] and (pg.time.get_ticks() - self.time_since_click)/1000 > self.click_cooldown and self is self.objects["Mouse"].over_element:
            self.time_since_click = pg.time.get_ticks()
            self.func()


class Font(Entity):
    def __init__(self, image: pg.Surface, include: list[int], step: int) -> None:
        super().__init__()
        self.characters = ["ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz", "0123456789", "!@#$%^&*()`~-_=+\\|[]}{';:/?.>,<"]
        self.font = self.load_font(image, include, step)
        self.z = 10000

    def load_font(self, font_img: pg.Surface, include: list[int], step: int):
        font_img.set_colorkey((0, 0, 0))
        characters = []
        font = {}
        x_pos = 0

        for x in range(font_img.get_width()):
            for y in range(font_img.get_height()):
                color = font_img.get_at((x, y))

                if color == (255, 0, 0, 255):
                    character = clip_img(font_img, x_pos, 0, x - x_pos, font_img.get_height())
                    x_pos = x + 1

                    if y == 1:
                        cp_surface = character.copy()
                        character = pg.Surface((cp_surface.get_width(), cp_surface.get_height() + step))
                        character.blit(cp_surface, (0, step))
                    characters.append(character)
        for i in include:
            for character in self.characters[i]:
                font[character] = characters[len(font)]
        return font

    def blit(self, target_name: str, text: str, x, y, space: int, size: int):
        x_pos = 0
        for letter in text:
            if letter == " ":
                x_pos += self.space * size
            else:
                character_img = pg.transform.scale_by(self.font[letter], size)
                self.objects["Renderer"].blit(self.z, target_name, character_img, (x + x_pos, y))
                x_pos += character_img.get_width() + size
