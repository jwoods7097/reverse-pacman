import pygame
from spritesheet import Spritesheet

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

    sprite_sheet = Spritesheet("pacman_sprites.png")
    base_state = sprite_sheet.parse_sprite("pacman_s.png")
    pacman_image_data = {'s': [base_state], 'right': [base_state], 'left': [base_state], 'down': [base_state], 'up': [base_state]}

    for i in range(2):
        pacman_image_data['right'].append(sprite_sheet.parse_sprite(f"pacman_right{i+1}.png"))
        pacman_image_data['left'].append(sprite_sheet.parse_sprite(f"pacman_left{i+1}.png"))
        pacman_image_data['down'].append(sprite_sheet.parse_sprite(f"pacman_down{i+1}.png"))
        pacman_image_data['up'].append(sprite_sheet.parse_sprite(f"pacman_up{i+1}.png"))

    events.invoke(events.LEVEL_UPDATE)

    # Game loop

    motion_index = 0
    index_direction = 0
    direction = 's'
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
                        direction = 'up'
                    if event.key == pygame.K_a:
                        pacman.turn(Direction.LEFT)
                        direction = 'left'
                    if event.key == pygame.K_s:
                        pacman.turn(Direction.DOWN)
                        direction = 'down'
                    if event.key == pygame.K_d:
                        pacman.turn(Direction.RIGHT)
                        direction = 'right'

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
                #pygame.draw.circle(screen, "yellow", *utils.circle(pacman.x,pacman.y,TILE_PIXEL_SIZE/2))
                screen.blit(pacman_image_data[direction][motion_index], (TILE_PIXEL_SIZE*pacman.x, TILE_PIXEL_SIZE*pacman.y))

                # Draw text
                score_text = font.render(f'Score: {pacman.score}', True, 'white')
                screen.blit(score_text, score_text.get_rect())

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

                pygame.display.update()
        
        if pacman.can_move(game):
            pacman.move()
            pacman.eat(game[pacman.y, pacman.x])
            game[pacman.y, pacman.x] = Tile.EMPTY

            print(f"Rounded: ({pacman.x}, {pacman.y})")
            print(f"Actual: ({pacman._x}, {pacman._y})\n")

        clock.tick(FPS)

    pygame.display.quit()
    pygame.quit()
    exit()
