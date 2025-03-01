from enum import Enum
import math
import random

from entity import Entity, Direction

class Mode(Enum):
    CHASE = 0
    SCATTER = 1
    FRIGHTENED = 2

# Base Ghost class, do not instantiate
class Ghost(Entity):

    mode = Mode.SCATTER

    def __init__(self, start_x, start_y):
        super().__init__(start_x, start_y)
        self.scatter_target = (0,0)

    # Gets the direction that would put the ghost closest to the point (x, y)
    def set_closest_dir(self, level, x, y):
        # Compute all distances
        distances = {
            Direction.RIGHT: math.dist([self.x + 1, self.y], [x, y]),
            Direction.UP:    math.dist([self.x, self.y - 1], [x, y]),
            Direction.LEFT:  math.dist([self.x - 1, self.y], [x, y]),
            Direction.DOWN:  math.dist([self.x, self.y + 1], [x, y])
        }

        # Filter out invalid movement directions
        for dir in list(Direction)[1:]:
            if not self.check_direction(level, dir) or dir == Direction.opposite(self.cur_dir):
                distances.pop(dir)

        # Set direction to closest distance to point
        self.cur_dir = min(distances, key=distances.get)
    
# Red Ghost
class Blinky(Ghost):

    def __init__(self, start_x, start_y):
        super().__init__(start_x, start_y)
        self.speed = 0.75
        self.scatter_target = (25,0)

    def set_dir(self, level, pacman_x, pacman_y):
        if Ghost.mode == Mode.CHASE:
            self.set_closest_dir(level, pacman_x, pacman_y)
        elif Ghost.mode == Mode.SCATTER:
            self.set_closest_dir(level, *self.scatter_target)
        else:
            self.cur_dir = random.choice(list(Direction)[1:])