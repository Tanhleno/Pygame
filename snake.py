import pygame as pg
from field import Point
from food import Food


class Snake:
    def __init__(self, color, field):
        self.field = field
        self.skin = pg.Surface((field.unity.get_width(),
                                field.unity.get_height()))
        self.skin.fill(color)
        self.color = color
        self.skeleton = []
        head = field.get_random_not_occupied_point()
        self._increase(head)
        self.direction = pg.Vector2(0, 0)
        self.dead = False

    def restart(self):
        while len(self.skeleton):
            self._destroy()
        head = self.field.get_random_not_occupied_point()
        self._increase(head)
        self.direction.update(0, 0)
        self.dead = False

    def set_direction(self, x, y):
        if len(self.skeleton) == 1 or self.direction.rotate(180) != pg.Vector2(x, y):
            self.direction.update(x, y)

    def set_direction_top(self):
        self.set_direction(0, -1)

    def set_direction_down(self):
        self.set_direction(0, 1)

    def set_direction_left(self):
        self.set_direction(-1, 0)

    def set_direction_right(self):
        self.set_direction(1, 0)

    def _increase(self, point):
        self.field.occupy(point, self)
        self.skeleton.append(point)
        self.field.draw_element(point, self.skin)
    
    def _decrease(self, point):
        self.field.not_occupy(point)
        del self.skeleton[0]
        self.field.draw_element(point, None)

    def _destroy(self):
        point = self.skeleton[-1]
        self.field.not_occupy(point)
        del self.skeleton[-1]
        self.field.draw_element(point, None)
    
    def _get_next_point(self):
        x = (self.skeleton[-1].x + self.direction.x) % self.field.get_width()
        y = (self.skeleton[-1].y + self.direction.y) % self.field.get_height()
        if x < 0:
            x += self.field.get_width()
        if y < 0:
            y += self.field.get_height()
        return Point(x, y)
    
    def update(self):
        if self.dead:
            self.restart()
        else:
            self.move()
    
    def move(self):
        if self.direction.x or self.direction.y:
            while True:
                next_point = self._get_next_point()
                owner = self.field.get_owner(next_point)
                if not owner:
                    break
                if type(owner) == Food:
                    owner.next_position()
                    self._increase(next_point)
                else:
                    self.dead = True
                    return
            self._increase(next_point)
            tail = self.skeleton[0]
            self._decrease(tail)
