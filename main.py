import pygame

from globals import *
from level import Level, Tile
from entity import Direction
from pacman import Pacman
from ghost import Ghost, Mode, Blinky, Clyde, Inky, Pinky
import utils
import events
import math
import time
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

    colliding = distance < (2 * universal_radius)
    return colliding

def place_ghosts(ghosts):
    # outside and on top
    (ghosts["blinky"].x, ghosts["blinky"].y) = GHOST_LEAVE_POS
    ghosts["blinky"].prison = False
    ghosts["inky"].pellet_count = 0

    (ghosts["inky"].x, ghosts["inky"].y) = (13,16)
    ghosts["inky"].prison = True
    ghosts["inky"].pellet_count = 0
    (ghosts["clyde"].x, ghosts["clyde"].y) = (14,16)
    ghosts["clyde"].prison = True
    ghosts["clyde"].pellet_count = 0
    (ghosts["pinky"].x, ghosts["pinky"].y) = (15,16)
    ghosts["pinky"].prison = True
    ghosts["pinky"].pellet_count = 0

def on_collide_handler(ghosts):
    # move ghosts
    place_ghosts(ghosts)
    # reset pellet counts
    ghosts_list = [ghosts[key] for key in ghosts.keys()]
    for ghost in ghosts_list:
        ghost.pellet_count = 0

def on_fright_collide_handler(ghosts):
    pass

def animate_death_pacman():
    # Draw death screen
    screen.fill("black")
    # Draw text
    score_text = font.render(f'Score: {pacman.score}', True, 'white')
    screen.blit(score_text, score_text.get_rect())

    # Draw life counter
    lives_text = font.render("Lives : " + str(pacman.lives), True, pacman.color)
    screen.blit(lives_text,(10*TILE_PIXEL_SIZE,0))                
    pygame.display.update()

    # Draw level
    for y, row in enumerate(game.board):
        for x, tile in enumerate(row):
            if tile == Tile.WALL:
                pygame.draw.rect(screen, "blue", utils.square(x,y,TILE_PIXEL_SIZE))
            elif tile == Tile.PELLET:
                pygame.draw.circle(screen, "white", *utils.circle(x,y,TILE_PIXEL_SIZE/5))
            elif tile == Tile.POWER_PELLET:
                pygame.draw.circle(screen, "white", *utils.circle(x,y,2*TILE_PIXEL_SIZE/5))
            elif tile == Tile.FRUIT:
                pygame.draw.circle(screen, "red", *utils.circle(x,y,2*TILE_PIXEL_SIZE/10))
    
    
    pass # Tim this is for you

def release_ghost_from_prison(next_ghost):
    if next_ghost.pellet_count >= next_ghost.pellet_max:
        (next_ghost.x, next_ghost.y) = GHOST_LEAVE_POS
        next_ghost.prison = False
        next_ghost.next_dir = Direction.DOWN
        return True
    else:
        return False

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
    clyde = Clyde(13,16)
    inky = Inky(14,16)
    pinky = Pinky(15,16)
    next_ghost_out = pinky
    ghosts = { "blinky": blinky, "inky": inky, "clyde": clyde, "pinky": pinky }

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
            def set_ghost_mode(mode):
                Ghost.mode = mode
                for ghost in ghosts.values():
                    ghost.reverse_direction()

            time_elapsed = tick_counter / FPS
            if time_elapsed <= 7:
                set_ghost_mode(Mode.SCATTER)
            elif time_elapsed <= 27:
                set_ghost_mode(Mode.CHASE)
            elif time_elapsed <= 34:
                set_ghost_mode(Mode.SCATTER)
            elif time_elapsed <= 54:
                set_ghost_mode(Mode.CHASE)
            elif time_elapsed <= 59:
                set_ghost_mode(Mode.SCATTER)
            elif time_elapsed <= 79:
                set_ghost_mode(Mode.CHASE)
            elif time_elapsed <= 84:
                set_ghost_mode(Mode.SCATTER)
            else:
                set_ghost_mode(Mode.CHASE)
            
            # if we release a ghost, then we have to know what ghost to release next
            # the first one we will always release is pinky, then inky, then clyde
            if next_ghost_out.prison and release_ghost_from_prison(next_ghost_out):
                if pinky.prison: next_ghost_out = pinky
                elif inky.prison: next_ghost_out = inky
                elif clyde.prison: next_ghost_out = clyde

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
                        elif tile == Tile.FRUIT:
                            pygame.draw.circle(screen, "red", *utils.circle(x,y,2*TILE_PIXEL_SIZE/10))

                # Draw pacman and ghosts
                pygame.draw.circle(screen, pacman.color, *utils.circle(pacman.x, pacman.y, TILE_PIXEL_SIZE/2))
                pygame.draw.circle(screen, blinky.color, *utils.circle(blinky.x, blinky.y, TILE_PIXEL_SIZE / 2))
                pygame.draw.circle(screen, inky.color, *utils.circle(inky.x, inky.y, TILE_PIXEL_SIZE / 2))
                pygame.draw.circle(screen, clyde.color, *utils.circle(clyde.x, clyde.y, TILE_PIXEL_SIZE / 2))
                pygame.draw.circle(screen, pinky.color, *utils.circle(pinky.x, pinky.y, TILE_PIXEL_SIZE / 2))
                
                # Draw text
                score_text = font.render(f'Score: {pacman.score}', True, 'white')
                screen.blit(score_text, score_text.get_rect())

                # Draw life counter
                lives_text = font.render("Lives : " + str(pacman.lives), True, pacman.color)
                screen.blit(lives_text,(10*TILE_PIXEL_SIZE,0))                
                pygame.display.update()

        # Move pacman
        if pacman.can_move(game):
            pacman.move()
            score_added = pacman.eat(game[pacman.y, pacman.x])
            if score_added > 0:
                next_ghost_out.pellet_count_up()
            game[pacman.y, pacman.x] = Tile.EMPTY
            if (pacman._dotsEaten == 70 or pacman._dotsEaten == 170):
                game.board[20, 13] = Tile.FRUIT

        # Move ghosts
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
                next_ghost_out = pinky
                pacman.lives -= 1
                animate_death_pacman()
                
                if pacman.lives == 0:
                    # ACTUAL GAME OVER --- MASSIVE NEGATIVE REWARD
                    game_over_text = font.render("---GAME OVER---", True, "red")
                    game_over_rect = game_over_text.get_rect()
                    screen.blit(game_over_text,(10*TILE_PIXEL_SIZE,2*TILE_PIXEL_SIZE))
                    pygame.display.update()
                    time.sleep(10)
                    running = False
                else:
                    # Lost Life, goes to reset --- MINOR NEGATIVE REWARD
                    time_elapsed = 0
                    # reset time so phases change
                    game_over_text = font.render("---  Ready?  ---", True, "red")
                    game_over_rect = game_over_text.get_rect()
                    screen.blit(game_over_text,(10*TILE_PIXEL_SIZE,2*TILE_PIXEL_SIZE))
                    pygame.display.update()
                    time.sleep(7)

        
        
        tick_counter += 1
        clock.tick(FPS)

    exit()
