from enum import Enum

from level import Tile
from globals import LEVEL_HEIGHT, LEVEL_WIDTH


class Direction(Enum):
    RIGHT = 0
    UP = 1
    LEFT = 2
    DOWN = 3

    @classmethod
    def opposite(self, direction):
        return Direction((direction.value + 2) % 4)


class Entity:

    def __init__(self, start_x, start_y):
        self._x = start_x
        self._y = start_y
        self.speed = 1.0
        self.cur_dir = Direction.LEFT
        self.next_dir = Direction.LEFT
        self.color = "white"

    @property
    def x(self):
        return int(self._x)

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return int(self._y)

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value

    def check_direction(self, level, direction):
        if direction == Direction.UP:
            return self.y <= 0 or level[self.y - 1, self.x] != Tile.WALL
        elif direction == Direction.LEFT:
            return self.x <= 0 or level[self.y, self.x - 1] != Tile.WALL
        elif direction == Direction.DOWN:
            return self.y + 1 >= LEVEL_HEIGHT or level[self.y + 1, self.x] != Tile.WALL
        elif direction == Direction.RIGHT:
            return self.x + 1 >= LEVEL_WIDTH or level[self.y, self.x + 1] != Tile.WALL
        else:
            return False

    def can_move(self, level):
        if self.check_direction(level, self.next_dir):
            self.cur_dir = self.next_dir
            return True
        return self.check_direction(level, self.cur_dir)

    def move(self):
        if self.cur_dir == Direction.RIGHT:
            self._x += self.speed
            if self.x >= LEVEL_WIDTH:
                self.x = 0
        elif self.cur_dir == Direction.UP:
            self._y -= self.speed
            if self.y < 0:
                self.y = LEVEL_HEIGHT - 1
        elif self.cur_dir == Direction.LEFT:
            self._x -= self.speed
            if self.x < 0:
                self.x = LEVEL_WIDTH - 1
        elif self.cur_dir == Direction.DOWN:
            self._y += self.speed
            if self.y >= LEVEL_HEIGHT:
                self.y = 0

    def turn(self, direction):
        self.next_dir = direction

    def reverse_direction(self):
        self.turn(Direction.opposite(self.cur_dir))

    def get_velocity(self):
        if self.cur_dir == Direction.RIGHT:
            return (self.speed, 0)
        elif self.cur_dir == Direction.UP:
            return (0, -self.speed)
        elif self.cur_dir == Direction.LEFT:
            return (-self.speed, 0)
        elif self.cur_dir == Direction.DOWN:
            return (0, self.speed)
        else:
            return (0, 0)
