from tkinter import Menu
import pygame
from spritesheet import Spritesheet
from globals import *
from level import Level, Tile
from entity import Direction
from pacman import Pacman
from gamestate import GameState
from ghost import Ghost, Mode, Blinky, Clyde, Inky, Pinky
import utils
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
    screen = pygame.display.set_mode((LEVEL_WIDTH*TILE_PIXEL_SIZE, LEVEL_HEIGHT*TILE_PIXEL_SIZE), pygame.SCALED | pygame.FULLSCREEN)
    pygame.display.set_caption("Reverse Pacman")
    clock = pygame.time.Clock()
    font = pygame.font.Font('assets/fonts/emulogic.ttf', 10)    
    title_font = pygame.font.Font('assets/fonts/emulogic.ttf', 10)

    running = True
    state = GameState()
    state = GameState.MENU

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

    sprite_sheet = Spritesheet("assets/sprites/pacman_sprites.png")
    ghost_fruit_sprite_sheet = Spritesheet("assets/sprites/ghost_fruit_sprites.png")
    base_state = sprite_sheet.parse_sprite("pacman_s.png")
    pacman_image_data = {d: [base_state] for d in Direction}
    ghost_image_data = {ghost: {d: [] for d in Direction} for ghost in ghosts}

    for i in range(2):
        for d in Direction:
            pacman_image_data[d].append(sprite_sheet.parse_sprite(f"pacman_{d.value}{i+1}.png"))

        for name in ghosts:
            for d in Direction:
                ghost_image_data[name][d].append(ghost_fruit_sprite_sheet.parse_sprite(f"{name}_{d.value}{i + 1}.png"))

    cherry = ghost_fruit_sprite_sheet.parse_sprite("cherry.png")

    # Game loop
    motion_index = 0
    ghost_motion_index = 0
    index_direction = 0
    
    while running:
        if state == GameState.MENU:
            screen.fill("black")
            # pygame.draw.rect(screen, "blue", utils.rect(START_BTN_X,START_BTN_Y,START_BTN_W,START_BTN_H))
            title_text = title_font.render(f'PRESS ANY BUTTON TO START', True, 'white')
            screen.blit(title_text, title_text.get_rect())
            pygame.display.update()
            queue = pygame.event.get()
            for event in queue:
                if event.type == pygame.KEYDOWN:
                    state = GameState.INGAME
            continue

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
            
        # Set ghost movement directions
        blinky.set_dir(game, pacman.x, pacman.y)
        inky.set_dir(game, pacman.x, pacman.y, blinky.x, blinky.y, pacman.cur_dir)
        clyde.set_dir(game, pacman.x, pacman.y)
        pinky.set_dir(game, pacman.x, pacman.y, pacman.cur_dir)
        
        # Set ghost mode
        def set_ghost_mode(mode):
            if Ghost.mode != mode:
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
        
        # Draw level
        screen.fill("black")
        for y, row in enumerate(game.board):
            for x, tile in enumerate(row):
                if tile == Tile.WALL:
                    pygame.draw.rect(screen, "blue", utils.square(x,y,TILE_PIXEL_SIZE))
                elif tile == Tile.PELLET:
                    pygame.draw.circle(screen, "white", *utils.circle(x,y,TILE_PIXEL_SIZE/5))
                elif tile == Tile.POWER_PELLET:
                    pygame.draw.circle(screen, "white", *utils.circle(x,y,2*TILE_PIXEL_SIZE/5))
                elif tile == Tile.FRUIT:
                    screen.blit(cherry,(TILE_PIXEL_SIZE * x, TILE_PIXEL_SIZE * y))

        # Draw pacman
        screen.blit(pacman_image_data[pacman.cur_dir][motion_index], (TILE_PIXEL_SIZE*pacman.x, TILE_PIXEL_SIZE*pacman.y))

        # Draw ghosts
        screen.blit(ghost_image_data['blinky'][blinky.cur_dir][ghost_motion_index], (TILE_PIXEL_SIZE*blinky.x, TILE_PIXEL_SIZE*blinky.y))
        screen.blit(ghost_image_data['inky'][inky.cur_dir][ghost_motion_index], (TILE_PIXEL_SIZE*inky.x, TILE_PIXEL_SIZE*inky.y))
        screen.blit(ghost_image_data['pinky'][pinky.cur_dir][ghost_motion_index], (TILE_PIXEL_SIZE*pinky.x, TILE_PIXEL_SIZE*pinky.y))
        screen.blit(ghost_image_data['clyde'][clyde.cur_dir][ghost_motion_index], (TILE_PIXEL_SIZE*clyde.x, TILE_PIXEL_SIZE*clyde.y))

        if (index_direction == 0):
            motion_index += 1
            if (motion_index == 3):
                motion_index = 1
                index_direction = 1
        else:
            motion_index -= 1
            if (motion_index == -1):
                motion_index = 1
                index_direction = 0

        ghost_motion_index = (ghost_motion_index + 1) % 2
        
        # Draw text
        score_text = font.render(f'Score: {pacman.score}', True, 'white')
        screen.blit(score_text, score_text.get_rect())

        # Draw life counter
        lives_text = font.render("Lives : " + str(pacman.lives), True, pacman.color)
        screen.blit(lives_text,(10*TILE_PIXEL_SIZE,0))              
        
        pygame.display.update()      
        
        # Tick game
        tick_counter += 1
        clock.tick(FPS)

    exit()
