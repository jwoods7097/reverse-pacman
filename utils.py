import pygame

from globals import TILE_PIXEL_SIZE, LEVEL_HEIGHT, LEVEL_WIDTH
from entity import Direction
from level import Tile

# use as *args for pygame circles to draw them from top left corner like rectangles instead of center
def circle(x,y,r):
    return (TILE_PIXEL_SIZE*(x+0.5),TILE_PIXEL_SIZE*(y+0.5)), r

def square(x,y,w):
    return pygame.Rect(TILE_PIXEL_SIZE*x, TILE_PIXEL_SIZE*y, w, w)

def can_move(entity, level):
    if entity.direction == Direction.UP:
        return entity.y <= 0 or level.board[entity.y-1, entity.x] != Tile.WALL
    elif entity.direction == Direction.LEFT:
        return entity.x <= 0 or level.board[entity.y, entity.x-1] != Tile.WALL
    elif entity.direction == Direction.DOWN:
        return entity.y+1 >= LEVEL_HEIGHT or level.board[entity.y+1, entity.x] != Tile.WALL
    elif entity.direction == Direction.RIGHT:
        return entity.x+1 >= LEVEL_WIDTH or level.board[entity.y, entity.x+1] != Tile.WALL
    else:
        return False