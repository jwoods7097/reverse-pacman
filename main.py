import pygame
from spritesheet import Spritesheet
from globals import *
from level import Level, Tile
from entity import Direction
from pacman import Pacman
from ghost import Ghost, Mode, Blinky, Clyde, Inky, Pinky
import utils
import time


def detect_collision(pacman, ghost):
    return pacman.x == ghost.x and pacman.y == ghost.y


def place_ghost(ghost):
    (ghost.x, ghost.y) = (14, 16)
    ghost.prison = True


def place_ghosts(ghosts):
    # outside and on top
    (ghosts["blinky"].x, ghosts["blinky"].y) = (13, 14)
    ghosts["blinky"].prison = False
    ghosts["inky"].pellet_count = 0

    (ghosts["inky"].x, ghosts["inky"].y) = (13, 16)
    ghosts["inky"].prison = True
    ghosts["inky"].pellet_count = 0
    (ghosts["clyde"].x, ghosts["clyde"].y) = (14, 16)
    ghosts["clyde"].prison = True
    ghosts["clyde"].pellet_count = 0
    (ghosts["pinky"].x, ghosts["pinky"].y) = (15, 16)
    ghosts["pinky"].prison = True
    ghosts["pinky"].pellet_count = 0


def on_collide_handler(ghosts):
    # move ghosts
    place_ghosts(ghosts)
    # reset pellet counts
    ghosts_list = [ghosts[key] for key in ghosts.keys()]
    for ghost in ghosts_list:
        ghost.pellet_count = 0


def on_fright_collide_handler(pacman, ghost):
    place_ghost(ghost)
    ghost.fright = False
    pacman.score += pacman.ghost_multiplier * 200
    pacman.ghost_multiplier *= 2


def animate_death_pacman():
    # Draw death screen
    screen.fill("black")
    # Draw text
    score_text = font.render(f'Score: {pacman.score}', True, 'white')
    screen.blit(score_text, score_text.get_rect())

    # Draw life counter
    lives_text = font.render("Lives : " + str(pacman.lives), True, pacman.color)
    screen.blit(lives_text, (10 * TILE_PIXEL_SIZE, 0))
    pygame.display.update()

    # Draw level
    for y, row in enumerate(game.board):
        for x, tile in enumerate(row):
            if tile == Tile.WALL:
                pygame.draw.rect(screen, "blue", utils.square(x, y, TILE_PIXEL_SIZE))
            elif tile == Tile.PELLET:
                pygame.draw.circle(screen, "white", *utils.circle(x, y, TILE_PIXEL_SIZE / 5))
            elif tile == Tile.POWER_PELLET:
                pygame.draw.circle(screen, "white", *utils.circle(x, y, 2 * TILE_PIXEL_SIZE / 5))
            elif tile == Tile.FRUIT:
                screen.blit(cherry, (TILE_PIXEL_SIZE * x, TILE_PIXEL_SIZE * y))

    pass  # Tim this is for you


def release_ghost_from_prison(next_ghost):
    (next_ghost.x, next_ghost.y) = GHOST_LEAVE_POS
    next_ghost.prison = False


def redraw_screen(board):
    screen.fill("black")
    for y, row in enumerate(board):
        for x, tile in enumerate(row):
            if tile == Tile.WALL:
                pygame.draw.rect(screen, "blue", utils.square(x, y, TILE_PIXEL_SIZE))
            elif tile == Tile.PELLET:
                pygame.draw.circle(screen, "white", *utils.circle(x, y, TILE_PIXEL_SIZE / 5))
            elif tile == Tile.POWER_PELLET:
                pygame.draw.circle(screen, "white", *utils.circle(x, y, 2 * TILE_PIXEL_SIZE / 5))
            elif tile == Tile.FRUIT:
                screen.blit(cherry, (TILE_PIXEL_SIZE * x, TILE_PIXEL_SIZE * y))


def lerp(a, b, t):
    return (1-t) * a + b * t

def add_position_data(dictionary, name, old_x, old_y, x, y, transition_frame_count):
    dictionary[name] = [(old_x, old_y)] + [
        (lerp(old_x, x, t / transition_frame_count), lerp(old_y, y, t / transition_frame_count))
        for t in range(1, transition_frame_count + 1)]


# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GHOST_COLORS = {
    "blinky": (255, 0, 0),
    "pinky": (255, 105, 180),
    "inky": (0, 255, 255),
    "clyde": (255, 165, 0)
}

# Ghost layout grid positions
GHOST_POSITIONS = {
    (0, 0): "blinky",
    (1, 0): "pinky",
    (0, 1): "inky",
    (1, 1): "clyde"
}

def show_menu():
    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count() - 1, -1, -1)]
    for j in joysticks:
        j.init()

    selector_pos = [0, 0]
    assigned_ghosts = {}  # ghost_name: "P1", "CPU", etc.
    joystick_assignments = {}  # ghost_name: joystick id

    total_players = min(4, len(joysticks))
    current_player_index = 0  # 0 = Player 1, 1 = Player 2, etc.

    finished_selection = False

    running1 = True
    while running1:
        screen.fill(BLACK)

        # Header text (e.g., Player 1 select)
        if current_player_index < total_players:
            label = font.render(f"Player {current_player_index + 1} select", True, WHITE)
            screen.blit(label, (screen.get_width() // 2 - label.get_width() // 2, 30))
        else:
            label = font.render("Press ENTER to start!", True, WHITE)
            screen.blit(label, (screen.get_width() // 2 - label.get_width() // 2, 30))

        # Draw ghost boxes
        for (gx, gy), name in GHOST_POSITIONS.items():
            color = GHOST_COLORS[name]
            rect = pygame.Rect(50 + gx * 200, 150 + gy * 150, 150, 100)
            pygame.draw.rect(screen, color, rect)

            # Ghost name centered
            name_label = font.render(name, True, BLACK)
            screen.blit(name_label, name_label.get_rect(center=rect.center))

            # Corner text: P1, P2, etc or CPU
            if name in assigned_ghosts:
                tag = assigned_ghosts[name]
            else:
                tag = "CPU"
            tag_label = font.render(tag, True, BLACK)
            screen.blit(tag_label, (rect.x + 5, rect.y + 5))

        # Draw selector box if still assigning
        if current_player_index < total_players:
            sel_rect = pygame.Rect(50 + selector_pos[0] * 200, 150 + selector_pos[1] * 150, 150, 100)
            pygame.draw.rect(screen, WHITE, sel_rect, 3)

        for event in pygame.event.get():

            # Enter prints assignments
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:

                    return assigned_ghosts

            # Only allow selection if current player < total_players
            if current_player_index < total_players:
                joystick = joysticks[current_player_index]

                # Movement
                if event.type == pygame.JOYHATMOTION and event.joy == joystick.get_id():
                    dx, dy = event.value
                    selector_pos[0] = max(0, min(1, selector_pos[0] + dx))  # X: 0–1
                    selector_pos[1] = max(0, min(1, selector_pos[1] - dy))  # Y: 0–1

                # 'A' Button (button 0) to lock in ghost
                if event.type == pygame.JOYBUTTONDOWN and event.joy == joystick.get_id():
                    if event.button == 0:
                        selected_ghost = GHOST_POSITIONS.get(tuple(selector_pos))
                        if selected_ghost not in assigned_ghosts:
                            assigned_ghosts[selected_ghost] = f"P{current_player_index + 1}"
                            joystick_assignments[selected_ghost] = joystick.get_id()
                            current_player_index += 1

        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((LEVEL_WIDTH * TILE_PIXEL_SIZE, LEVEL_HEIGHT * TILE_PIXEL_SIZE),
                                     pygame.FULLSCREEN | pygame.SCALED)
    pygame.display.set_caption("Reverse Pacman")
    clock = pygame.time.Clock()
    font = pygame.font.Font('assets/fonts/emulogic.ttf', 10)

    joystick1 = pygame.joystick.Joystick(3)
    joystick2 = pygame.joystick.Joystick(2)
    joystick3 = pygame.joystick.Joystick(1)
    joystick4 = pygame.joystick.Joystick(0)

    running = True


    # Load level
    game = Level('assets/levels/level1.txt')

    # Load game objects
    pacman = Pacman(*PACMAN_LEAVE_POS)

    blinky = Blinky(13, 14)
    clyde = Clyde(13, 16)
    inky = Inky(14, 16)
    pinky = Pinky(15, 16)
    ghosts = {"blinky": blinky, "inky": inky, "clyde": clyde, "pinky": pinky}

    # Parse sprites
    sprite_sheet = Spritesheet("assets/sprites/pacman_sprites.png")
    ghost_fruit_sprite_sheet = Spritesheet("assets/sprites/ghost_fruit_sprites.png")
    base_state = sprite_sheet.parse_sprite("pacman_s.png")
    pacman_image_data = {d: [base_state] for d in Direction}
    ghost_image_data = {ghost: {d: [] for d in Direction} for ghost in ghosts}
    ghost_fright_image_data = [[], []]

    for i in range(2):
        for d in Direction:
            pacman_image_data[d].append(sprite_sheet.parse_sprite(f"pacman_{d.value}{i + 1}.png"))

        for name in ghosts:
            for d in Direction:
                ghost_image_data[name][d].append(ghost_fruit_sprite_sheet.parse_sprite(f"{name}_{d.value}{i + 1}.png"))

        for j in range(2):
            ghost_fright_image_data[i].append(ghost_fruit_sprite_sheet.parse_sprite(f"fright_{i}{j + 1}.png"))

    cherry = ghost_fruit_sprite_sheet.parse_sprite("cherry.png")

    assigned_ghosts = joysticks = joystick_assignments = show_menu()

    blinky_player = joystick_assignments.get("blinky")
    inky_player = joystick_assignments.get("inky")
    pinky_player = joystick_assignments.get("pinky")
    clyde_player = joystick_assignments.get("clyde")

    # Game loop
    motion_index = 0
    ghost_motion_index = 0
    index_direction = 0
    fright_end = 0
    tick_counter = 0
    transition_frame_count = 5
    position_data = {'pacman': [], 'blinky': [], 'inky': [], 'pinky': [], 'clyde': []}
    while running:
        queue = pygame.event.get()
        for event in queue:
            # Quit game if "X" in window is clicked
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                # Quit game if escape key is pressed
                if event.key == pygame.K_ESCAPE:
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


            if event.type == pygame.JOYHATMOTION:
                # Helper list to loop through joysticks and associated player labels
                joystick_players = [
                    (joystick1, "P1"),
                    (joystick2, "P2"),
                    (joystick3, "P3"),
                    (joystick4, "P4"),
                ]

                for joystick, player_id in joystick_players:
                    hat = joystick.get_hat(0)

                    if hat == (-1, 0):  # Left
                        if blinky_player == player_id:
                            blinky.turn(Direction.LEFT)
                        elif inky_player == player_id:
                            inky.turn(Direction.LEFT)
                        elif pinky_player == player_id:
                            pinky.turn(Direction.LEFT)
                        elif clyde_player == player_id:
                            clyde.turn(Direction.LEFT)

                    elif hat == (1, 0):  # Right
                        if blinky_player == player_id:
                            blinky.turn(Direction.RIGHT)
                        elif inky_player == player_id:
                            inky.turn(Direction.RIGHT)
                        elif pinky_player == player_id:
                            pinky.turn(Direction.RIGHT)
                        elif clyde_player == player_id:
                            clyde.turn(Direction.RIGHT)

                    elif hat == (0, 1):  # Up
                        if blinky_player == player_id:
                            blinky.turn(Direction.UP)
                        elif inky_player == player_id:
                            inky.turn(Direction.UP)
                        elif pinky_player == player_id:
                            pinky.turn(Direction.UP)
                        elif clyde_player == player_id:
                            clyde.turn(Direction.UP)

                    elif hat == (0, -1):  # Down
                        if blinky_player == player_id:
                            blinky.turn(Direction.DOWN)
                        elif inky_player == player_id:
                            inky.turn(Direction.DOWN)
                        elif pinky_player == player_id:
                            pinky.turn(Direction.DOWN)
                        elif clyde_player == player_id:
                            clyde.turn(Direction.DOWN)


        # Set ghost movement directions
        if blinky_player is None:
            blinky.set_dir(game, pacman.x, pacman.y)
        if inky_player is None:
            inky.set_dir(game, pacman.x, pacman.y, blinky.x, blinky.y, pacman.cur_dir)
        if clyde_player is None:
            clyde.set_dir(game, pacman.x, pacman.y)
        if pinky_player is None:
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

        if fright_end <= time_elapsed:
            for ghost in ghosts.values():
                ghost.fright = False
            pacman.ghost_multiplier = 1

        # if we release a ghost, then we have to know what ghost to release next
        # the first one we will always release is pinky, then inky, then clyde
        for ghost in ghosts.values():
            if ghost.prison and Ghost.pellet_count >= ghost.pellet_max:
                release_ghost_from_prison(ghost)

        # Move pacman
        if pacman.can_move(game):
            old_x = pacman.x
            old_y = pacman.y
            pacman.move()

            if (old_x == LEVEL_WIDTH - 1 and pacman.x == 0):
                add_position_data(position_data, 'pacman', old_x, old_y, LEVEL_WIDTH, pacman.y, transition_frame_count)
                position_data['pacman'][-1] = (pacman.x, pacman.y)
            elif (old_x == 0 and pacman.x == LEVEL_WIDTH - 1):
                add_position_data(position_data, 'pacman', old_x, old_y, -1, pacman.y, transition_frame_count)
                position_data['pacman'][-1] = (pacman.x, pacman.y)
            else:
                add_position_data(position_data, 'pacman', old_x, old_y, pacman.x, pacman.y, transition_frame_count)
            score_added = pacman.eat(game[pacman.y, pacman.x])
            if game[pacman.y, pacman.x] == Tile.PELLET:
                Ghost.pellet_count += 1
            elif game[pacman.y, pacman.x] == Tile.POWER_PELLET:
                for ghost in ghosts.values():
                    ghost.fright = True
                fright_end = time_elapsed + 6
            game[pacman.y, pacman.x] = Tile.EMPTY
            if (pacman._dotsEaten == 70 or pacman._dotsEaten == 170):
                game.board[20, 13] = Tile.FRUIT
        else:
            position_data['pacman'] = []


        # Detect collisions
        def check_collision():
            for ghost in ghosts.values():
                collide = detect_collision(pacman, ghost)

                if collide and ghost.fright:
                    on_fright_collide_handler(pacman, ghost)
                elif collide:
                    on_collide_handler(ghosts)
                    blinky.set_dir(game, pacman.x, pacman.y)
                    pacman.lives -= 1
                    animate_death_pacman()

                    if pacman.lives == 0:
                        # ACTUAL GAME OVER --- MASSIVE NEGATIVE REWARD
                        game_over_text = font.render("---GAME OVER---", True, "red")
                        game_over_rect = game_over_text.get_rect()
                        screen.blit(game_over_text, (10 * TILE_PIXEL_SIZE, 2 * TILE_PIXEL_SIZE))
                        pygame.display.update()
                        time.sleep(10)
                        global running
                        running = False

                    else:
                        # Lost Life, goes to reset --- MINOR NEGATIVE REWARD
                        global time_elapsed
                        time_elapsed = 0
                        Ghost.pellet_count = 0
                        for ghost in ghosts.values():
                            ghost.fright = False
                        # reset time so phases change
                        game_over_text = font.render("---Ready?---", True, "red")
                        game_over_rect = game_over_text.get_rect()
                        screen.blit(game_over_text, (10 * TILE_PIXEL_SIZE, 2 * TILE_PIXEL_SIZE))
                        (pacman.x, pacman.y) = PACMAN_LEAVE_POS
                        pygame.display.update()
                        time.sleep(5)


        check_collision()

        #Move ghosts
        for name, ghost in ghosts.items():
            old_x = ghost.x
            old_y = ghost.y
            if ghost.can_move(game):
                ghost.move()
                if (old_x == LEVEL_WIDTH - 1 and ghost.x == 0):
                    add_position_data(position_data, name, old_x, old_y, LEVEL_WIDTH, ghost.y, transition_frame_count)
                    position_data[name][-1] = (ghost.x, ghost.y)
                elif (old_x == 0 and ghost.x == LEVEL_WIDTH - 1):
                    add_position_data(position_data, name, old_x, old_y, -1, ghost.y, transition_frame_count)
                    position_data[name][-1] = (ghost.x, ghost.y)

            add_position_data(position_data, name, old_x, old_y, ghost.x, ghost.y, transition_frame_count)

        # Detect collisions
        check_collision()

        # Draw level
        redraw_screen(game.board)

        for t in range(0, transition_frame_count):
            redraw_screen(game.board)
            # Draw text
            score_text = font.render(f'Score: {pacman.score}', True, 'white')
            screen.blit(score_text, score_text.get_rect())

            # Draw life counter
            lives_text = font.render("Lives : " + str(pacman.lives), True, pacman.color)
            screen.blit(lives_text, (10 * TILE_PIXEL_SIZE, 0))

            if len(position_data['pacman']) > 0:
                # Draw pacman
                screen.blit(pacman_image_data[pacman.cur_dir][motion_index],
                            (round(TILE_PIXEL_SIZE * position_data['pacman'][t][0]),
                             round(TILE_PIXEL_SIZE * position_data['pacman'][t][1])))
            else:
                screen.blit(pacman_image_data[pacman.cur_dir][motion_index],
                            (TILE_PIXEL_SIZE * pacman.x,
                             TILE_PIXEL_SIZE * pacman.y))

            # Draw ghosts
            for name in ghosts:
                ghost = ghosts[name]

                if ghost.fright:
                    if fright_end - time_elapsed > 1:
                        screen.blit(ghost_fright_image_data[0][ghost_motion_index],
                                    (round(TILE_PIXEL_SIZE * position_data[name][t][0]),
                                     round(TILE_PIXEL_SIZE * position_data[name][t][1])))
                    else:
                        screen.blit(ghost_fright_image_data[ghost_motion_index][ghost_motion_index],
                                    (round(TILE_PIXEL_SIZE * position_data[name][t][0]),
                                     round(TILE_PIXEL_SIZE * position_data[name][t][1])))
                else:
                    screen.blit(ghost_image_data[name][ghost.cur_dir][ghost_motion_index],
                                (round(TILE_PIXEL_SIZE * position_data[name][t][0]),
                                 round(TILE_PIXEL_SIZE * position_data[name][t][1])))

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

            pygame.display.update()

        # Draw text
        score_text = font.render(f'Score: {pacman.score}', True, 'white')
        screen.blit(score_text, score_text.get_rect())

        # Draw life counter
        lives_text = font.render("Lives : " + str(pacman.lives), True, pacman.color)
        screen.blit(lives_text, (10 * TILE_PIXEL_SIZE, 0))

        if pacman._dotsEaten == 240:
            game_over_text = font.render("---YOU WIN---", True, "green")
            game_over_rect = game_over_text.get_rect()
            screen.blit(game_over_text, (10 * TILE_PIXEL_SIZE, 2 * TILE_PIXEL_SIZE))
            pygame.display.update()
            time.sleep(10)
            running = False

        pygame.display.update()

        # Tick game
        tick_counter += 1
        clock.tick(FPS)
