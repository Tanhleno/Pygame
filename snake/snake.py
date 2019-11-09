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
        head = field.get_random_not_occupied_point()
        field.occupy(head, self)
        field.draw_element(head, self.skin)
        self.skeleton = [head]
        self.stopped = True
        self.dead = False
        self.direction = pg.Vector2(0, 0)

    def change_direction(self, word):
        if word == 'top':
            self.direction.update(0, -1)
        elif word == 'right':
            self.direction.update(1, 0)
        elif word == 'down':
            self.direction.update(0, 1)
        elif word == 'left':
            self.direction.update(-1, 0)
        else:
            raise ValueError("changeDirection must be set with:" +
                             " 'top', 'right', 'left' or 'down'")
        self.stopped = False

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
            self._destroy()
        else:
            self.move()
    
    def move(self):
        if not self.stopped:
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
