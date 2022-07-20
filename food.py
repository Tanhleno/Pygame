from field import Field
import pygame as pg


class Food:
    def __init__(self, color, field, saturation=1):
        self.color = color
        self.skin = pg.Surface((field.unity.get_width(),
                                field.unity.get_height()))
        self.skin.fill(color)
        self.field = field
        self.saturation = saturation
        self.position = field.get_random_not_occupied_point()
        self.field.occupy(self.position, self)
        self.field.draw_element(self.position, self.skin)

    def next_position(self):
        temp = self.field.get_random_not_occupied_point()
        self.field.not_occupy(self.position)
        self.position = temp
        self.field.occupy(self.position, self)
        self.field.draw_element(self.position, self.skin)
