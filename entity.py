from enum import Enum

from globals import LEVEL_HEIGHT, LEVEL_WIDTH
import events

class Direction(Enum):
    NONE = 0
    RIGHT = 1
    UP = 2
    LEFT = 3
    DOWN = 4

class Entity:

    def __init__(self, start_x, start_y):
        self.x = start_x
        self.y = start_y
        self.speed = 1
        self.direction = Direction.NONE

    def move(self):
        if self.direction == Direction.RIGHT:
            self.x += self.speed
            if self.x >= LEVEL_WIDTH:
                self.x = 0
        elif self.direction == Direction.UP:
            self.y -= self.speed
            if self.y < 0:
                self.y = LEVEL_HEIGHT - 1
        elif self.direction == Direction.LEFT:
            self.x -= self.speed
            if self.x < 0:
                self.x = LEVEL_WIDTH - 1
        elif self.direction == Direction.DOWN:
            self.y += self.speed
            if self.y >= LEVEL_HEIGHT:
                self.y = 0
        
        events.invoke(events.LEVEL_UPDATE)

    def turn(self, direction):
        self.direction = direction
