import pygame

from globals import *
from level import Level, Tile
from entity import Direction
from pacman import Pacman
import utils
import events

if __name__ == '__main__':
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((LEVEL_WIDTH*TILE_PIXEL_SIZE, LEVEL_HEIGHT*TILE_PIXEL_SIZE))
    pygame.display.set_caption("Pacman")
    clock = pygame.time.Clock()
    font = pygame.font.Font('assets/fonts/emulogic.ttf', 10)
    running = True

    # Load level
    game = Level('assets/levels/level1.txt')

    # Load game objects
    pacman = Pacman(13, 26)

    events.invoke(events.LEVEL_UPDATE)

    # Game loop
    while running:      
        queue = pygame.event.get()
        for event in queue:
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                else:
                    # Pacman movement
                    if event.key == pygame.K_w:
                        pacman.turn(Direction.UP)
                    if event.key == pygame.K_a:
                        pacman.turn(Direction.LEFT)
                    if event.key == pygame.K_s:
                        pacman.turn(Direction.DOWN)
                    if event.key == pygame.K_d:
                        pacman.turn(Direction.RIGHT)

            if event.type == events.LEVEL_UPDATE:
                screen.fill("black")

                # Draw level
                for y, row in enumerate(game.board):
                    for x, tile in enumerate(row):
                        if tile == Tile.WALL:
                            pygame.draw.rect(screen, "blue", utils.square(x,y,TILE_PIXEL_SIZE))
                        elif tile == Tile.PELLET:
                            pygame.draw.circle(screen, "white", *utils.circle(x,y,TILE_PIXEL_SIZE/5))
                        elif tile == Tile.POWER_PELLET:
                            pygame.draw.circle(screen, "white", *utils.circle(x,y,2*TILE_PIXEL_SIZE/5))

                # Draw pacman
                pygame.draw.circle(screen, "yellow", *utils.circle(pacman.x,pacman.y,TILE_PIXEL_SIZE/2))

                # Draw text
                score_text = font.render(f'Score: {pacman.score}', True, 'white')
                screen.blit(score_text, score_text.get_rect())
                
                pygame.display.update()
        
        if utils.can_move(pacman, game):
            pacman.move()
            pacman.eat(game.board[pacman.y, pacman.x])
            game.board[pacman.y, pacman.x] = Tile.EMPTY

        clock.tick(FPS)

    pygame.display.quit()
    pygame.quit()
    exit()
