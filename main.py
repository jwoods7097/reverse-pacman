import pygame

from globals import *
from level import Level, Tile
import utils

# pygame setup
pygame.init()
screen = pygame.display.set_mode((28*TILE_PIXEL_SIZE, 36*TILE_PIXEL_SIZE))
clock = pygame.time.Clock()
running = True
update = True

# Load level
game = Level('level1.txt')
utils.invoke(LEVEL_UPDATE)

# Game loop
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False

        if event.type == LEVEL_UPDATE:
            # Redraw level
            for y, row in enumerate(game.board):
                for x, tile in enumerate(row):
                    if tile == Tile.Wall:
                        pygame.draw.rect(screen, "blue", utils.square(x,y,TILE_PIXEL_SIZE))
                    elif tile == Tile.Pellet:
                        pygame.draw.circle(screen, "white", *utils.circle(x,y,TILE_PIXEL_SIZE/5))
                    elif tile == Tile.PowerPellet:
                        pygame.draw.circle(screen, "white", *utils.circle(x,y,2*TILE_PIXEL_SIZE/5))

            pygame.display.update()
    
    clock.tick(30)

pygame.display.quit()
pygame.quit()
exit()
