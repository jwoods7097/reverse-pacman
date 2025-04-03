from entity import Entity
from level import Tile
import globals

class Pacman(Entity):
    
    def __init__(self, start_x, start_y):
        super().__init__(start_x, start_y)
        self.score = 0
        self.timer = 0
        self.color = "yellow"
        self._dotsEaten = 0
        self.lives = 3
        self.ghost_multiplier = 1

    @property
    def energized(self):
        return self._energized

    @energized.setter
    def energized(self, is_energized):
        self._energized = is_energized

    def dotsEaten(self):
        return self._dotsEaten

    def eat(self, tile_type):
        if tile_type == Tile.PELLET:
            self.score += 10
            self._dotsEaten += 1
            return 10
        elif tile_type == Tile.POWER_PELLET:
            self.score += 50
            return 50
        elif tile_type == Tile.FRUIT:
            self.score += 100
            return 100
        else:
            return 0
