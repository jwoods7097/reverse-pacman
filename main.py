import pygame

from globals import *
from level import Level, Tile
from entity import Direction
from pacman import Pacman
from ghost import Blinky
from ghost import Inky
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
    blinky = Blinky(13, 14)
    inky = Inky(14, 14)
    events.invoke(events.LEVEL_UPDATE)
    currentDirection = "none"
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
                        currentDirection = "up"
                    if event.key == pygame.K_a:
                        pacman.turn(Direction.LEFT)
                        currentDirection = "left"
                    if event.key == pygame.K_s:
                        pacman.turn(Direction.DOWN)
                        currentDirection = "down"
                    if event.key == pygame.K_d:
                        pacman.turn(Direction.RIGHT)
                        currentDirection = "right"

            blinky.set_dir(game, pacman.x, pacman.y)
            inky.set_dir(game, pacman.x, pacman.y, blinky.x, blinky.y, pacman.cur_dir)


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

                # Draw pacman and ghosts
                pygame.draw.circle(screen, "yellow", *utils.circle(pacman.x, pacman.y, TILE_PIXEL_SIZE/2))
                pygame.draw.circle(screen, "red", *utils.circle(blinky.x, blinky.y, TILE_PIXEL_SIZE / 2))
                pygame.draw.circle(screen, "cyan", *utils.circle(inky.x, inky.y, TILE_PIXEL_SIZE / 2))
                # Draw text
                score_text = font.render(f'Score: {pacman.score}', True, 'white')
                screen.blit(score_text, score_text.get_rect())
                
                pygame.display.update()
        
        if pacman.can_move(game):
            pacman.move()
            pacman.eat(game[pacman.y, pacman.x])
            game[pacman.y, pacman.x] = Tile.EMPTY

            print(f"Rounded: ({pacman.x}, {pacman.y})")
            print(f"Actual: ({pacman._x}, {pacman._y})\n")
            print(f"Direction: {currentDirection}")
            print(f"blinky: {blinky.x}, {blinky.y}\n")
            print(f"inky: {inky.x}, {inky.y}\n")
        if blinky.can_move(game):
            blinky.move()
        if inky.can_move(game):
            inky.move()
        clock.tick(FPS)

    pygame.display.quit()
    pygame.quit()
    exit()
