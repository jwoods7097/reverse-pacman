import pygame

from globals import *
from level import Level, Tile
from entity import Direction
from pacman import Pacman
from ghost import Blinky, Clyde, Inky, Pinky
import utils
import events
import math

def detect_collision(circle_A, circle_B):
    """
    Return boolean if colliding

    If euclidian distance from two circles is shorter than their radii combined
    then they must be colliding.
    """
    dx = (circle_A.x - circle_B.x)*TILE_PIXEL_SIZE
    dy = (circle_A.y - circle_B.y)*TILE_PIXEL_SIZE
    distance = math.sqrt(dx * dx + dy * dy)
    universal_radius = TILE_PIXEL_SIZE/2
    print(f"Distance: {distance}, Radiusx2: {universal_radius}")

    colliding = distance < (2 * universal_radius)
    return colliding

def place_ghosts(ghosts):
    # outside and on top
    (ghosts["blinky"].x, ghosts["blinky"].y) = GHOST_LEAVE_POS

    (ghosts["inky"].x, ghosts["inky"].y) = (13,16)
    (ghosts["clyde"].x, ghosts["clyde"].y) = (14,16)
    (ghosts["pinky"].x, ghosts["pinky"].y) = (15,16)

def on_collide_handler(ghosts):
    place_ghosts(ghosts)
    pass
def on_fright_collide_handler(ghosts):
    pass


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
    clyde = Clyde(13,16)
    inky = Inky(14,16)
    pinky = Pinky(15,16)
    ghosts = { "blinky": blinky, "inky": inky, "clyde": clyde, "pinky": pinky }

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
                    if event.key == pygame.K_a:
                        pacman.turn(Direction.LEFT)
                    if event.key == pygame.K_s:
                        pacman.turn(Direction.DOWN)
                    if event.key == pygame.K_d:
                        pacman.turn(Direction.RIGHT)

            blinky.set_dir(game, pacman.x, pacman.y, pacman.energized)
            inky.set_dir(game, pacman.x, pacman.y, blinky.x, blinky.y, pacman.cur_dir, pacman)
            clyde.set_dir(game, pacman.x, pacman.y, clyde.x, clyde.y)
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
                pygame.draw.circle(screen, "yellow", *utils.circle(pacman.x, pacman.y, TILE_PIXEL_SIZE/2))
                pygame.draw.circle(screen, blinky.color, *utils.circle(blinky.x, blinky.y, TILE_PIXEL_SIZE / 2))
                pygame.draw.circle(screen, inky.color, *utils.circle(inky.x, inky.y, TILE_PIXEL_SIZE / 2))
                pygame.draw.circle(screen, clyde.color, *utils.circle(clyde.x, clyde.y, TILE_PIXEL_SIZE / 2))
                pygame.draw.circle(screen, pinky.color, *utils.circle(pinky.x, pinky.y, TILE_PIXEL_SIZE / 2))
                # Draw text
                score_text = font.render(f'Score: {pacman.score}', True, 'white')
                screen.blit(score_text, score_text.get_rect())
                
                pygame.display.update()

        if pacman.can_move(game):
            pacman.move()
            pacman.eat(game[pacman.y, pacman.x])
            game[pacman.y, pacman.x] = Tile.EMPTY
            #DEBUG PRINTS
            #print(f"pacman: ({pacman.x}, {pacman.y})")
            #print(f"Direction: {pacman.cur_dir}")
            #print(f"blinky: {blinky.x}, {blinky.y}\n")
            #print(f"inky: {inky.x}, {inky.y}\n")
            #print(f"clyde: {clyde.x}, {clyde.y}\n")
            #print(f"pinky: {pinky.x}, {pinky.y}\n")

        if blinky.can_move(game):
            blinky.move()
        if inky.can_move(game):
            inky.move()
        if clyde.can_move(game):
            clyde.move()
        if pinky.can_move(game):
            pinky.move()

        # Detect collisions
        
        for key in ghosts.keys():
            ghost = ghosts[key]
            collide = detect_collision(pacman, ghost)

            if collide and ghost.get_fright(): 
                on_fright_collide_handler(ghosts)
            elif collide:
                on_collide_handler(ghosts)
        
        # old collision detection        
        # if pacman.x == blinky.x and pacman.y == blinky.y:
        #     running = False
        # elif pacman.x == inky.x and pacman.y == inky.y:
        #     running = False
        # elif pacman.x == clyde.x and pacman.y == clyde.y:
        #     running = False
        # elif pacman.x == pinky.x and pacman.y == pinky.y:
        #     running = False
        tick_counter += 1
        clock.tick(FPS)

    exit()


