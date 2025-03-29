import pygame

from globals import *
from level import Level, Tile
from entity import Direction
from pacman import Pacman
from ghost import Ghost, Mode, Blinky, Clyde, Inky, Pinky
import utils
import events

if __name__ == '__main__':
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((LEVEL_WIDTH*TILE_PIXEL_SIZE, LEVEL_HEIGHT*TILE_PIXEL_SIZE))
    pygame.display.set_caption("Reverse Pacman")
    clock = pygame.time.Clock()
    font = pygame.font.Font('assets/fonts/emulogic.ttf', 10)
    running = True

    # Load level
    game = Level('assets/levels/level1.txt')

    # Load game objects
    pacman = Pacman(13, 26)
    blinky = Blinky(13, 14)
    clyde = Clyde(15, 14)
    inky = Inky(14, 14)
    pinky = Pinky(16, 14)
    
    events.invoke(events.LEVEL_UPDATE)
    
    # Game loop
    while running:      
        queue = pygame.event.get()
        for event in queue:
            # Quit game if "X" in window is clicked
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                # Quit game if "q" is pressed
                if event.key == pygame.K_q:
                    running = False
                else:
                    # Set pacman movement direction
                    if event.key == pygame.K_w:
                        pacman.turn(Direction.UP)
                    if event.key == pygame.K_a:
                        pacman.turn(Direction.LEFT)
                    if event.key == pygame.K_s:
                        pacman.turn(Direction.DOWN)
                    if event.key == pygame.K_d:
                        pacman.turn(Direction.RIGHT)

            # Set ghost mode
            time_elapsed = tick_counter / FPS
            if time_elapsed <= 7:
                Ghost.mode = Mode.SCATTER
            elif time_elapsed <= 27:
                Ghost.mode = Mode.CHASE
            elif time_elapsed <= 34:
                Ghost.mode = Mode.SCATTER
            elif time_elapsed <= 54:
                Ghost.mode = Mode.CHASE
            elif time_elapsed <= 59:
                Ghost.mode = Mode.SCATTER
            elif time_elapsed <= 79:
                Ghost.mode = Mode.CHASE
            elif time_elapsed <= 84:
                Ghost.mode = Mode.SCATTER
            else:
                Ghost.mode = Mode.CHASE

            print(time_elapsed, Ghost.mode)
            
            # Set ghost movement directions
            blinky.set_dir(game, pacman.x, pacman.y)
            inky.set_dir(game, pacman.x, pacman.y, blinky.x, blinky.y, pacman.cur_dir)
            clyde.set_dir(game, pacman.x, pacman.y)
            pinky.set_dir(game, pacman.x, pacman.y, pacman.cur_dir)
            
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
                pygame.draw.circle(screen, pacman.color, *utils.circle(pacman.x, pacman.y, TILE_PIXEL_SIZE/2))
                pygame.draw.circle(screen, blinky.color, *utils.circle(blinky.x, blinky.y, TILE_PIXEL_SIZE / 2))
                pygame.draw.circle(screen, inky.color, *utils.circle(inky.x, inky.y, TILE_PIXEL_SIZE / 2))
                pygame.draw.circle(screen, clyde.color, *utils.circle(clyde.x, clyde.y, TILE_PIXEL_SIZE / 2))
                pygame.draw.circle(screen, pinky.color, *utils.circle(pinky.x, pinky.y, TILE_PIXEL_SIZE / 2))
                
                # Draw text
                score_text = font.render(f'Score: {pacman.score}', True, 'white')
                screen.blit(score_text, score_text.get_rect())
                
                pygame.display.update()

        # Move pacman
        if pacman.can_move(game):
            pacman.move()
            pacman.eat(game[pacman.y, pacman.x])
            game[pacman.y, pacman.x] = Tile.EMPTY

        # Move ghosts
        if blinky.can_move(game):
            blinky.move()
        if inky.can_move(game):
            inky.move()
        if clyde.can_move(game):
            clyde.move()
        if pinky.can_move(game):
            pinky.move()

        # Kill pacman and end game if it runs into a ghost
        if pacman.x == blinky.x and pacman.y == blinky.y:
            running = False
        elif pacman.x == inky.x and pacman.y == inky.y:
            running = False
        elif pacman.x == clyde.x and pacman.y == clyde.y:
            running = False
        elif pacman.x == pinky.x and pacman.y == pinky.y:
            running = False
        
        tick_counter += 1
        clock.tick(FPS)

    exit()
