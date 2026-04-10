import pygame as pg

from .entity import Entity, EntityGroup

class Mouse(Entity):
    def __init__(self, ui_elements: EntityGroup) -> None:
        super().__init__(True)
        self.display = self.objects["Display"]

        self.display_pos: pg.Vector2 = pg.Vector2()
        self.ui_elements = ui_elements

        self.z = 100
        self.target = "display"

    @property
    def over_element(self) -> Entity | None:
        highest_element = None
        for ui_element in self.ui_elements:
            if ui_element.rect.collidepoint(self.pos) and (highest_element == None or highest_element.z < ui_element.z ):
                highest_element = ui_element

        return highest_element

    def update(self) -> None:
        # Update mouse position on the window
        self.pos.x, self.pos.y = pg.mouse.get_pos()

        # Update mouse position on the display
        self.display_pos.x = (self.pos.x - self.display.pos.x)/self.display.scale
        self.display_pos.y = (self.pos.y - self.display.pos.y)/self.display.scale

    def select(self) -> None:
        self.pos.x, self.pos.y = pg.mouse.get_pos()
