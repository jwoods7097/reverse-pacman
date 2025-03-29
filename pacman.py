from entity import Entity
from level import Tile
import globals

#from ghost import Clyde, Blinky, Inky, Pinky, Mode
class Pacman(Entity):
    def __init__(self, start_x, start_y):
        super().__init__(start_x, start_y)
        self.score = 0
        self.timer = 0

    def eat(self, type):
        if type == Tile.PELLET:
            self.score += 10
            return 10
        elif type == Tile.POWER_PELLET:
            self.score += 50
            self.timer = globals.tick_counter
            globals.energized = True
            return 50
        elif type == Tile.FRUIT:
            # TODO: Add multiple types of fruit
            self.score += 100
            return 100
