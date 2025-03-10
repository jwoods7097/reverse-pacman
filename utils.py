import pygame

from globals import TILE_PIXEL_SIZE, LEVEL_HEIGHT, LEVEL_WIDTH
from entity import Direction
from level import Tile

# use as *args for pygame circles to draw them from top left corner like rectangles instead of center
def circle(x,y,r):
    return (TILE_PIXEL_SIZE*(x+0.5),TILE_PIXEL_SIZE*(y+0.5)), r

def square(x,y,w):
    return pygame.Rect(TILE_PIXEL_SIZE*x, TILE_PIXEL_SIZE*y, w, w)

def rect(x,y,w,h):
    return pygame.Rect(TILE_PIXEL_SIZE*x, TILE_PIXEL_SIZE*y, w, h)
