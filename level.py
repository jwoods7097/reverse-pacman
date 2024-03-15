import numpy as np
from enum import Enum

class Tile(Enum):
  Empty = 0
  Wall = 1
  Pellet = 2
  PowerPellet = 3
  Fruit = 4

class Level:

  def __init__(self, level_file):
    self.board = np.zeros((36, 28), dtype=Tile)

    with open(level_file, 'r') as file:
      for y, line in enumerate(file):
        line = line.strip()
        for x, char in enumerate(line):
          if char == '_':
            self.board[y, x] = Tile.Empty
          elif char == 'x':
            self.board[y, x] = Tile.Wall
          elif char == '.':
            self.board[y, x] = Tile.Pellet
          elif char == 'f':
            self.board[y, x] = Tile.Fruit
          elif char == 'o':
            self.board[y, x] = Tile.PowerPellet
          else:
            raise ValueError('Invalid file formatting')
