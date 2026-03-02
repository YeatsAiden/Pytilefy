import pygame

class Display(pg.Sprite):
    def __init__(self, w, h):
        pg.Sprite.__init__(self)
        self.image = pg.Surface(w, h)
        self.rect = pg.FRect(0, 0, w, h)
        self.fill_color = pg.Color(0, 0, 0, 255)

    def draws f


