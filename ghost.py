from enum import Enum

from entity import Entity, Direction

class Mode(Enum):
    CHASE = 0
    SCATTER = 1
    FRIGHTENED = 2

# Default ghost has behavior of Blinky
class Ghost(Entity):

    def __init__(self, start_x, start_y):
        super().__init__(start_x, start_y)
        self.scatter_target = (25,0)
        self.mode = Mode.CHASE

    def get_dir(self, pacman_x, pacman_y):
        return Direction.LEFT
    