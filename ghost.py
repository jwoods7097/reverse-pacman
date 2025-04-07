from enum import Enum
import math
import random
from entity import Entity, Direction
from globals import *


class Mode(Enum):
    CHASE = 0
    SCATTER = 1
    FRIGHTENED = 2


# Base Ghost class, do not instantiate
class Ghost(Entity):
    mode = Mode.SCATTER
    fright = False

    def __init__(self, start_x, start_y, init_color):
        super().__init__(start_x, start_y)
        self.scatter_target = (0, 0)
        self.init_color = init_color
        self.color = self.init_color
        self.pellet_count = 0
        self.pellet_max = 0
        self.prison = True

    def update_color(self):
        if Ghost.mode == Mode.FRIGHTENED:
            temp_timer = tick_counter
            if (tick_counter - temp_timer) > 7 and (temp_timer - tick_counter) % 2 == 1:
                self.color = "white"
            else:
                self.color = "blue"
        else:
            self.color = self.init_color

    # Gets the direction that would put the ghost closest to the point (x, y)
    def set_closest_dir(self, level, x, y):
        # Compute all distances
        distances = {
            Direction.UP: math.dist([self.x, self.y - 1], [x, y]),
            Direction.LEFT: math.dist([self.x - 1, self.y], [x, y]),
            Direction.DOWN: math.dist([self.x, self.y + 1], [x, y]),
            Direction.RIGHT: math.dist([self.x + 1, self.y], [x, y])
        }

        # Filter out invalid movement directions
        for dir in list(Direction):
            if not self.check_direction(level, dir) or dir == Direction.opposite(self.cur_dir):
                distances.pop(dir)

        # Set direction to closest distance to point
        self.turn(min(distances, key=distances.get))

    def turn_random_dir(self, level):
        directions = list(Direction)

        # Filter out invalid movement directions
        for dir in directions:
            if not self.check_direction(level, dir) or dir == Direction.opposite(self.cur_dir):
                directions.remove(dir)

        self.turn(random.choice(directions))

    def get_fright(self):
        if self.mode == Mode.FRIGHTENED:
            self.fright = True
        return self.fright
    
    def get_pellet_count(self):
        return self.pellet_count
    
    def pellet_count_up(self):
        self.pellet_count += 1


# Red Ghost
class Blinky(Ghost):

    def __init__(self, start_x, start_y):
        super().__init__(start_x, start_y, "red")
        self.speed = 1.0
        self.scatter_target = (25, 0)
        self.color = "red"

    def set_dir(self, level, pacman_x, pacman_y):
        if Ghost.mode == Mode.CHASE:
            self.set_closest_dir(level, pacman_x, pacman_y)
        elif Ghost.mode == Mode.SCATTER:
            self.set_closest_dir(level, *self.scatter_target)
        else:
            self.turn_random_dir(level)


class Inky(Ghost):
    def __init__(self, start_x, start_y):
        super().__init__(start_x, start_y, "cyan")
        self.speed = 1.0
        self.scatter_target = (27, 34)
        self.color = "cyan"
        self.pellet_max = 30

    def set_dir(self, level, pacman_x, pacman_y, blinky_x, blinky_y, pacman_dir):
        if Ghost.mode == Mode.CHASE:
            # Draws a vector from pacman + offset for every direciton to blinky and doubles it.
            if pacman_dir == Direction.UP:
                target_x = blinky_x + 2 * ((pacman_x - 2) - blinky_x)
                target_y = blinky_y + 2 * ((pacman_y - 2) - blinky_y)
            elif pacman_dir == Direction.DOWN:
                target_x = blinky_x + 2 * (pacman_x - blinky_x)
                target_y = blinky_y + 2 * ((pacman_y + 2) - blinky_y)
            elif pacman_dir == Direction.LEFT:
                target_x = blinky_x + 2 * ((pacman_x - 2) - blinky_x)
                target_y = blinky_y + 2 * (pacman_y - blinky_y)
            elif pacman_dir == Direction.RIGHT:
                target_x = blinky_x + 2 * ((pacman_x + 2) - blinky_x)
                target_y = blinky_y + 2 * (pacman_y - blinky_y)
            self.set_closest_dir(level, target_x, target_y)
        elif Ghost.mode == Mode.SCATTER:
            self.set_closest_dir(level, *self.scatter_target)
        else:
            self.turn_random_dir(level)


class Clyde(Ghost):
    def __init__(self, start_x, start_y):
        super().__init__(start_x, start_y, "orange")
        self.speed = 1.0
        self.scatter_target = (0, 34)
        self.color = "orange"
        self.pellet_max = 60

    def set_dir(self, level, pacman_x, pacman_y):
        if Ghost.mode == Mode.CHASE:
            if math.dist((pacman_x, pacman_y), (self.x, self.y)) >= 8:
                self.set_closest_dir(level, pacman_x, pacman_y)
            else:
                self.set_closest_dir(level, *self.scatter_target)
        elif Ghost.mode == Mode.SCATTER:
            self.set_closest_dir(level, *self.scatter_target)
        else:
            self.turn_random_dir(level)


class Pinky(Ghost):
    def __init__(self, start_x, start_y):
        super().__init__(start_x, start_y, "pink")
        self.speed = 1.0
        self.scatter_target = (2, 0)
        self.color = "pink"
        self.pellet_max = 5

    def set_dir(self, level, pacman_x, pacman_y, pacman_dir):
        if Ghost.mode == Mode.CHASE:
            if pacman_dir == Direction.UP:
                target_x = pacman_x - 4
                target_y = pacman_y - 4
            elif pacman_dir == Direction.DOWN:
                target_x = pacman_x
                target_y = pacman_y + 4
            elif pacman_dir == Direction.LEFT:
                target_x = pacman_x - 4
                target_y = pacman_y
            elif pacman_dir == Direction.RIGHT:
                target_x = pacman_x + 4
                target_y = pacman_y
            self.set_closest_dir(level, target_x, target_y)
        elif Ghost.mode == Mode.SCATTER:
            self.set_closest_dir(level, *self.scatter_target)
        elif Ghost.mode == Mode.FRIGHTENED:
            self.turn_random_dir(level)
