import pygame as pg
import random
from collections import namedtuple

Margin = namedtuple("Margin", ['left', 'top'])
Point = namedtuple("Point", ['x', 'y'])


class Field:
    def __init__(self, screen, unity):
        self.screen = screen
        self.unity = unity
        left = (screen.get_width() % unity.get_width()) // 2
        top = (screen.get_height() % unity.get_height()) // 2
        self.margin = Margin(left, top)

        self.occupied = dict()
        self.not_occupied = set()
        for x in range(screen.get_width() // unity.get_width()):
            for y in range(screen.get_height() // unity.get_height()):
                self.not_occupied.add(Point(x, y))
    
    def get_rect(self, point):
        left = point.x * self.unity.get_width() + self.margin.left
        top = point.y * self.unity.get_height() + self.margin.top
        return pg.rect.Rect(left, top, self.unity.get_width(), self.unity.get_height())

    def draw_element(self, point, surface=None):
        if not surface:
            surface = self.unity
        new_rect = self.screen.blit(surface, self.get_rect(point))
        pg.display.update(new_rect)

    def occupy(self, point, reference):
        try:
            self.not_occupied.remove(point)
        except KeyError:
            pass
        self.occupied[point] = reference

    def not_occupy(self, point):
        try:
            del self.occupied[point]
        except KeyError:
            pass
        self.not_occupied.add(point)
    
    def get_random_not_occupied_point(self):
        return random.choice(list(self.not_occupied))
    
    def get_owner(self, point):
        try:
            return self.occupied[point]
        except KeyError:
            return None
    
    def get_width(self):
        return self.screen.get_width() // self.unity.get_width()

    def get_height(self):
        return self.screen.get_height() // self.unity.get_height()
