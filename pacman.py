from entity import Entity
from level import Tile
from globals import *

class Pacman(Entity):
    
    def __init__(self, start_x, start_y):
        super().__init__(start_x, start_y)
        self.score = 0
        self._energized = False
        self.timer = 0
        self._dotsEaten = 0
    @property
    def energized(self):
        return self._energized

    @energized.setter
    def energized(self, is_energized):
        self._energized = is_energized

    def dotsEaten(self):
        return self._dotsEaten


    def eat(self, type):
        if type == Tile.PELLET:
            self.score += 10
            self._dotsEaten += 1
            
            return 10
        elif type == Tile.POWER_PELLET:
            self.score += 50
            self.timer = tick_counter
            self.energized = True
            return 50
        elif type == Tile.FRUIT:
            self.score += 100
            return 100