import pygame as pg


# I swear this wasn't stolen
class Renderer:
    def __init__(self, groups) -> None:
        self.groups = groups
        self.queue: dict[str, list] = {group: [] for group in self.groups}
        self.order: int = 0

    def clear(self):
        self.order = 0
        for group in self.groups:
            self.queue[group] = []

    def render(self, z: int, group: str, surface: pg.Surface, position):
        self.queue[group].append([z, self.order, surface, position])
        self.order += 1

    def render_sprites(self, surfaces: dict[str, pg.Surface]):
        for group, surface in surfaces.items():
            if group in self.queue:
                self.queue[group].sort()
                for sprite in self.queue[group]:
                    surface.blit(sprite[2], sprite[3])
