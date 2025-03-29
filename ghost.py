from enum import Enum
import math
import random
from entity import Entity, Direction
from globals import *
from pacman import Pacman


class Mode(Enum):
    CHASE = 0
    SCATTER = 1
    FRIGHTENED = 2


# Base Ghost class, do not instantiate
class Ghost(Entity):
    mode = Mode.SCATTER

    def __init__(self, start_x, start_y, init_color):
        super().__init__(start_x, start_y)
        self.scatter_target = (0, 0)
        self.init_color = init_color
        self.color = self.init_color

    def update_color(self):
        if self.mode == Mode.FRIGHTENED:
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
            Direction.RIGHT: math.dist([self.x + 1, self.y], [x, y]),
            Direction.UP: math.dist([self.x, self.y - 1], [x, y]),
            Direction.LEFT: math.dist([self.x - 1, self.y], [x, y]),
            Direction.DOWN: math.dist([self.x, self.y + 1], [x, y])
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
        super().__init__(start_x, start_y, "red")
        self.speed = 0.75
        self.scatter_target = (25, 0)
        self.color = "red"

    def set_dir(self, level, pacman_x, pacman_y, energized):
        if energized:
            self.mode = Mode.FRIGHTENED
            self.update_color()
        else:
            self.mode = Mode.CHASE

        if self.mode == Mode.CHASE:
            self.set_closest_dir(level, pacman_x, pacman_y)
        elif self.mode == Mode.SCATTER:
            self.set_closest_dir(level, *self.scatter_target)
        else:
            self.cur_dir = random.choice(list(Direction)[1:])


class Inky(Ghost):
    def __init__(self, start_x, start_y):
        super().__init__(start_x, start_y, "cyan")
        self.speed = 0.75
        self.scatter_target = (27, 34)
        self.color = "cyan"

    def set_dir(self, level, pacman_x, pacman_y, blinky_x, blinky_y, pacman_dir, energized):
        if energized:
            self.mode = Mode.FRIGHTENED
        else:
            set.mode = Mode.CHASE

        if self.mode == Mode.CHASE:
            if pacman_dir == Direction.UP:  # Draws a vector from pacman + offset for every direciton to blinky and doubles it.
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
            else:
                target_x, target_y = self.x, self.y  # Stay in place if no valid direction found

            self.set_closest_dir(level, target_x, target_y)
            #print(f"Inky target: {target_x}, {target_y}")
        elif self.mode == Mode.SCATTER:
            self.set_closest_dir(level, *self.scatter_target)
        else:
            self.cur_dir = random.choice(list(Direction)[1:])


class Clyde(Ghost):
    def __init__(self, start_x, start_y):
        super().__init__(start_x, start_y, "orange")
        self.speed = 0.75
        self.scatter_target = (0, 34)
        self.color = "orange"

    def set_dir(self, level, pacman_x, pacman_y, clyde_x, clyde_y):

        if math.sqrt(math.pow(pacman_x - clyde_x, 2) + math.pow(pacman_y - clyde_y, 2)) >= 8:
            self.mode = Mode.CHASE
        else:
            self.mode = Mode.SCATTER

        if Ghost.mode == Mode.CHASE:
            self.set_closest_dir(level, pacman_x, pacman_y)
        elif Ghost.mode == Mode.SCATTER:
            self.set_closest_dir(level, *self.scatter_target)
        elif Ghost.mode == Mode.FRIGHTENED:
            self.cur_dir = random.choice(list(Direction)[1:])


class Pinky(Ghost):
    def __init__(self, start_x, start_y):
        super().__init__(start_x, start_y, "pink")
        self.speed = 0.75
        self.scatter_target = (0, 0)
        self.color = "pink"

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
            else:
                target_x, target_y = self.x, self.y  # Stay in place if no valid direction found
            self.set_closest_dir(level, target_x, target_y)
            #print(f"Pinky target: {target_x}, {target_y}")
            #print(f"Pacman location: {pacman_x}, {pacman_y}")
        elif Ghost.mode == Mode.SCATTER:
            self.set_closest_dir(level, *self.scatter_target)
        elif Ghost.mode == Mode.FRIGHTENED:
            self.cur_dir = random.choice(list(Direction)[1:])
