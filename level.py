import numpy as np
from enum import Enum

from globals import LEVEL_HEIGHT, LEVEL_WIDTH

class Tile(Enum):
    EMPTY = 0
    WALL = 1
    PELLET = 2
    POWER_PELLET = 3
    FRUIT = 4

class Level:

    def __init__(self, level_file):
        self.board = np.zeros((LEVEL_HEIGHT, LEVEL_WIDTH), dtype=Tile)

        with open(level_file, 'r') as file:
            for y, line in enumerate(file):
                line = line.strip()
                for x, char in enumerate(line):
                    if char == '_':
                        self.board[y, x] = Tile.EMPTY
                    elif char == 'x':
                        self.board[y, x] = Tile.WALL
                    elif char == '.':
                        self.board[y, x] = Tile.PELLET
                    elif char == 'f':
                        self.board[y, x] = Tile.FRUIT
                    elif char == 'o':
                        self.board[y, x] = Tile.POWER_PELLET
                    else:
                        raise ValueError('Invalid file formatting')
                    
    def __getitem__(self, index):
        y, x = index
        if y < 0 or y >= LEVEL_HEIGHT or x < 0 or x >= LEVEL_WIDTH:
            raise IndexError("Index out of range")
        return self.board[y, x]
    
    def __setitem__(self, index, value):
        y, x = index
        if y < 0 or y >= LEVEL_HEIGHT or x < 0 or x >= LEVEL_WIDTH:
            raise IndexError("Index out of range")
        self.board[y, x] = value
