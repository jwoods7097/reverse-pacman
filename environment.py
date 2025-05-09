import gymnasium as gym
import math
import numpy as np
import pygame
import utils
import time

from entity import Direction
from ghost import Ghost, Mode, Blinky, Clyde, Inky, Pinky
from gymnasium import spaces
from gymnasium.envs.registration import register
#from globals import LEVEL_HEIGHT, LEVEL_WIDTH, TILE_PIXEL_SIZE
from globals import *
from level import Level, Tile
from main import on_collide_handler, on_fright_collide_handler, animate_death_pacman, release_ghost_from_prison, detect_collision, place_ghost, place_ghosts, redraw_screen, lerp, add_position_data
from pacman import Pacman
from spritesheet import Spritesheet

class PacmanEnv(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": FPS}

    def __init__(self, render_mode=None):
        
        self.level = Level('assets/levels/level1.txt')

        # Encodes data about pacman's location, the ghosts' location, and the level state
        self.observation_space = spaces.Dict(
            {
                # for entities, we are storing (x, y, v_x, v_y)
                "pacman": spaces.Box(np.array([0, 0, -1, -1]), np.array([LEVEL_HEIGHT, LEVEL_WIDTH, 1, 1]), dtype=np.float32),
                "blinky": spaces.Box(np.array([0, 0, -1, -1]), np.array([LEVEL_HEIGHT, LEVEL_WIDTH, 1, 1]), dtype=np.float32),
                "inky":   spaces.Box(np.array([0, 0, -1, -1]), np.array([LEVEL_HEIGHT, LEVEL_WIDTH, 1, 1]), dtype=np.float32),
                "pinky":  spaces.Box(np.array([0, 0, -1, -1]), np.array([LEVEL_HEIGHT, LEVEL_WIDTH, 1, 1]), dtype=np.float32),
                "clyde":  spaces.Box(np.array([0, 0, -1, -1]), np.array([LEVEL_HEIGHT, LEVEL_WIDTH, 1, 1]), dtype=np.float32),
                "level":  spaces.MultiBinary([LEVEL_HEIGHT, LEVEL_WIDTH, len(Tile)])
            }
        )

        # The 4 actions are: left, up, right, down
        self.action_space = spaces.Discrete(4)
        
        # Pygame objects
        pygame.init()
        self.window = None
        self.clock = None
        self.font = None

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

    def _get_obs(self):  
        level_obs = np.zeros((LEVEL_HEIGHT, LEVEL_WIDTH, len(Tile)), dtype=bool)
        for y, row in enumerate(self.level.board):
            for x, tile in enumerate(row):
                level_obs[y, x, tile.value] = True

        return {
                # for entities, we are storing (x, y, v_x, v_y)
                "pacman": [self.pacman.x, self.pacman.y, *self.pacman.get_velocity()],
                "blinky": [self.ghosts["blinky"].x, self.ghosts["blinky"].y, *self.ghosts["blinky"].get_velocity()],
                "inky":   [self.ghosts["inky"].x, self.ghosts["inky"].y, *self.ghosts["inky"].get_velocity()],
                "pinky":  [self.ghosts["pinky"].x, self.ghosts["pinky"].y, *self.ghosts["pinky"].get_velocity()],
                "clyde":  [self.ghosts["clyde"].x, self.ghosts["clyde"].y, *self.ghosts["clyde"].get_velocity()],
                "level":  level_obs
            }

    def _get_info(self):
        return {
            "step": self.episode_step,
            "score": self.pacman.score
        }

    def reset(self, seed=None, options=None):
        # We need the following line to seed self.np_random
        super().reset(seed=seed)

        # Game objects
        self.pacman = Pacman(*PACMAN_LEAVE_POS)

        self.blinky = Blinky(13, 14)
        self.clyde = Clyde(13,16)
        self.inky = Inky(14,16)
        self.pinky = Pinky(15,16)
        self.ghosts = {"blinky": self.blinky, "inky": self.inky, "clyde": self.clyde, "pinky": self.pinky}
        
        self.level = Level('assets/levels/level1.txt')

        self.motion_index = 0
        self.ghost_motion_index = 0
        self.index_direction = 0
        self.fright_end = 0
        #self.tick_counter = 0
        self.time_elapsed = 0
        self.transition_frame_count = 5
        self.position_data = {'pacman': [], 'blinky': [], 'inky':[], 'pinky':[], 'clyde':[]}

        self.episode_step = 0

        observation = self._get_obs()
        info = self._get_info()

        return observation, info

    def step(self, action):
        self.episode_step += 1

        # Process agent action
        direction = Direction(action)
        self.pacman.turn(direction)

        # Punish Pacman a bit for not eating pellets
        reward = -1
        terminated = False

        self.blinky.set_dir(self.level, self.pacman.x, self.pacman.y)
        self.inky.set_dir(self.level, self.pacman.x, self.pacman.y, self.blinky.x, self.blinky.y, self.pacman.cur_dir)
        self.clyde.set_dir(self.level, self.pacman.x, self.pacman.y)
        self.pinky.set_dir(self.level, self.pacman.x, self.pacman.y, self.pacman.cur_dir)

        self.choose_ghost_mode()

        """# if we release a ghost, then we have to know what ghost to release next
        # the first one we will always release is pinky, then inky, then clyde
        if next_ghost_out.prison and self.release_ghost_from_prison(next_ghost_out):
            if self.pinky.prison: next_ghost_out = self.pinky
            elif self.inky.prison: next_ghost_out = self.inky
            elif self.clyde.prison: next_ghost_out = self.clyde"""

        if self.fright_end <= self.time_elapsed:
            for ghost in self.ghosts.values():
                ghost.fright = False
            self.pacman.ghost_multiplier = 1
        
        # if we release a ghost, then we have to know what ghost to release next
        # the first one we will always release is pinky, then inky, then clyde
        for ghost in self.ghosts.values():
            if ghost.prison and Ghost.pellet_count >= ghost.pellet_max:
                release_ghost_from_prison(ghost)

        # Move pacman
        if self.pacman.can_move(self.level):
            old_x = self.pacman.x
            old_y = self.pacman.y
            self.pacman.move()

            if (old_x == LEVEL_WIDTH - 1 and self.pacman.x == 0):
                add_position_data(self.position_data, 'pacman', old_x, old_y, LEVEL_WIDTH, self.pacman.y, self.transition_frame_count)
                self.position_data['pacman'][-1] = (self.pacman.x, self.pacman.y)
            elif (old_x == 0 and self.pacman.x == LEVEL_WIDTH - 1):
                add_position_data(self.position_data, 'pacman', old_x, old_y, -1, self.pacman.y, self.transition_frame_count)
                self.position_data['pacman'][-1] = (self.pacman.x, self.pacman.y)
            else:
                add_position_data(self.position_data, 'pacman', old_x, old_y, self.pacman.x, self.pacman.y, self.transition_frame_count)
            reward = self.pacman.eat(self.level[self.pacman.y, self.pacman.x])
            if self.level[self.pacman.y, self.pacman.x] == Tile.PELLET:
                Ghost.pellet_count += 1
            elif self.level[self.pacman.y, self.pacman.x] == Tile.POWER_PELLET:
                for ghost in self.ghosts.values():
                    ghost.fright = True
                self.fright_end = self.time_elapsed + 6
            self.level[self.pacman.y, self.pacman.x] = Tile.EMPTY
            if (self.pacman._dotsEaten == 70 or self.pacman._dotsEaten == 170):
                self.level.board[20, 13] = Tile.FRUIT
        else:
            self.position_data['pacman'] = []

        # Detect collisions
        def check_collision():
            nonlocal reward
            nonlocal terminated
            for ghost in self.ghosts.values():
                collide = detect_collision(self.pacman, ghost)

                if collide and ghost.fright:
                    on_fright_collide_handler(self.pacman, ghost)
                    reward = self.pacman.ghost_multiplier * 200
                elif collide:
                    on_collide_handler(self.ghosts)
                    self.blinky.set_dir(self.level, self.pacman.x, self.pacman.y)
                    self.pacman.lives -= 1
                    reward = -1000

                    if self.pacman.lives == 0:
                        # ACTUAL GAME OVER --- MASSIVE NEGATIVE REWARD
                        terminated = True
                    else:
                        # Lost Life, goes to reset --- MINOR NEGATIVE REWARD
                        self.time_elapsed = 0
                        Ghost.pellet_count = 0
                        for ghost in self.ghosts.values():
                            ghost.fright = False
                        (self.pacman.x, self.pacman.y) = PACMAN_LEAVE_POS

        check_collision()

        #Move ghosts
        for name, ghost in self.ghosts.items():
            if ghost.can_move(self.level):
                old_x = ghost.x
                old_y = ghost.y
                ghost.move()
                if (old_x == LEVEL_WIDTH - 1 and ghost.x == 0):
                    add_position_data(self.position_data, name, old_x, old_y, LEVEL_WIDTH, ghost.y, self.transition_frame_count)
                    self.position_data[name][-1] = (ghost.x, ghost.y)
                elif (old_x == 0 and ghost.x == LEVEL_WIDTH - 1):
                    add_position_data(self.position_data, name, old_x, old_y, -1, ghost.y, self.transition_frame_count)
                    self.position_data[name][-1] = (ghost.x, ghost.y)
                else:
                    add_position_data(self.position_data, name, old_x, old_y, ghost.x, ghost.y, self.transition_frame_count)

        # Detect collisions
        check_collision()
        
        if self.pacman._dotsEaten == 240:
            reward = 1000000
            terminated = True

        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation, reward, terminated, False, info
    
    def render(self):
        if self.render_mode == "human":
            return self._render_frame()
        
    def _render_frame(self):
        # Initialization of pygame objects
        if self.window is None and self.render_mode == "human":
            pygame.init()
            self.window = pygame.display.set_mode((LEVEL_WIDTH * TILE_PIXEL_SIZE, LEVEL_HEIGHT * TILE_PIXEL_SIZE), pygame.FULLSCREEN | pygame.SCALED)
            pygame.display.set_caption("Reverse Pacman")
            
            sprite_sheet = Spritesheet("assets/sprites/pacman_sprites.png")
            ghost_fruit_sprite_sheet = Spritesheet("assets/sprites/ghost_fruit_sprites.png")
            base_state = sprite_sheet.parse_sprite("pacman_s.png")
            self.pacman_image_data = {d: [base_state] for d in Direction}
            self.ghost_image_data = {ghost: {d: [] for d in Direction} for ghost in self.ghosts}
            self.ghost_fright_image_data = [[], []]

            for i in range(2):
                for d in Direction:
                    self.pacman_image_data[d].append(sprite_sheet.parse_sprite(f"pacman_{d.value}{i+1}.png"))

                for name in self.ghosts:
                    for d in Direction:
                        self.ghost_image_data[name][d].append(ghost_fruit_sprite_sheet.parse_sprite(f"{name}_{d.value}{i + 1}.png"))
                
                for j in range(2):
                    self.ghost_fright_image_data[i].append(ghost_fruit_sprite_sheet.parse_sprite(f"fright_{i}{j + 1}.png"))

            self.cherry = ghost_fruit_sprite_sheet.parse_sprite("cherry.png")
        if self.clock is None and self.render_mode == "human":
            self.clock = pygame.time.Clock()
        if self.font is None and self.render_mode == "human":
            self.font = pygame.font.Font('assets/fonts/emulogic.ttf', 10)

        # Draw level
        for t in range(0, self.transition_frame_count):
            self.window.fill("black")
            for y, row in enumerate(self.level.board):
                for x, tile in enumerate(row):
                    if tile == Tile.WALL:
                        pygame.draw.rect(self.window, "blue", utils.square(x, y, TILE_PIXEL_SIZE))
                    elif tile == Tile.PELLET:
                        pygame.draw.circle(self.window, "white", *utils.circle(x, y, TILE_PIXEL_SIZE / 5))
                    elif tile == Tile.POWER_PELLET:
                        pygame.draw.circle(self.window, "white", *utils.circle(x, y, 2 * TILE_PIXEL_SIZE / 5))
                    elif tile == Tile.FRUIT:
                        self.window.blit(self.cherry, (TILE_PIXEL_SIZE * x, TILE_PIXEL_SIZE * y))
            
            # Draw text
            score_text = self.font.render(f'Score: {self.pacman.score}', True, 'white')
            self.window.blit(score_text, score_text.get_rect())

            # Draw life counter
            lives_text = self.font.render("Lives : " + str(self.pacman.lives), True, self.pacman.color)
            self.window.blit(lives_text, (10 * TILE_PIXEL_SIZE, 0))

            if len(self.position_data['pacman']) > 0:
                # Draw pacman
                self.window.blit(self.pacman_image_data[self.pacman.cur_dir][self.motion_index],
                            (round(TILE_PIXEL_SIZE * self.position_data['pacman'][t][0]),
                             round(TILE_PIXEL_SIZE * self.position_data['pacman'][t][1])))
            else:
                self.window.blit(self.pacman_image_data[self.pacman.cur_dir][self.motion_index],
                            (TILE_PIXEL_SIZE * self.pacman.x,
                             TILE_PIXEL_SIZE * self.pacman.y))

            # Draw ghosts
            for name in self.ghosts:
                ghost = self.ghosts[name]
                if ghost.fright:
                    if self.fright_end - self.time_elapsed > 1:
                        self.window.blit(self.ghost_fright_image_data[0][self.ghost_motion_index],
                                    (round(TILE_PIXEL_SIZE * self.position_data[name][t][0]),
                                     round(TILE_PIXEL_SIZE * self.position_data[name][t][1])))
                    else:
                        self.window.blit(self.ghost_fright_image_data[self.ghost_motion_index][self.ghost_motion_index],
                                    (round(TILE_PIXEL_SIZE * self.position_data[name][t][0]),
                                     round(TILE_PIXEL_SIZE * self.position_data[name][t][1])))
                else:
                    self.window.blit(self.ghost_image_data[name][ghost.cur_dir][self.ghost_motion_index],
                                (round(TILE_PIXEL_SIZE * self.position_data[name][t][0]),
                                 round(TILE_PIXEL_SIZE * self.position_data[name][t][1])))

            if (self.index_direction == 0):
                self.motion_index += 1
                if (self.motion_index == 3):
                    self.motion_index = 1
                    self.index_direction = 1
            else:
                self.motion_index -= 1
                if (self.motion_index == -1):
                    self.motion_index = 1
                    self.index_direction = 0

            self.ghost_motion_index = (self.ghost_motion_index + 1) % 2

            pygame.display.update()

        # Draw text
        score_text = self.font.render(f'Score: {self.pacman.score}', True, 'white')
        self.window.blit(score_text, score_text.get_rect())

        # Draw life counter
        lives_text = self.font.render("Lives : " + str(self.pacman.lives), True, self.pacman.color)
        self.window.blit(lives_text, (10 * TILE_PIXEL_SIZE, 0))
        
        # Update display
        pygame.event.pump()
        pygame.display.update()
        self.clock.tick(self.metadata["render_fps"])

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()
        exit()
    
    def choose_ghost_mode(self):
        self.time_elapsed = self.episode_step / FPS
        if self.time_elapsed <= 7:
            self.set_ghost_mode(Mode.SCATTER)
        elif self.time_elapsed <= 27:
            self.set_ghost_mode(Mode.CHASE)
        elif self.time_elapsed <= 34:
            self.set_ghost_mode(Mode.SCATTER)
        elif self.time_elapsed <= 54:
            self.set_ghost_mode(Mode.CHASE)
        elif self.time_elapsed <= 59:
            self.set_ghost_mode(Mode.SCATTER)
        elif self.time_elapsed <= 79:
            self.set_ghost_mode(Mode.CHASE)
        elif self.time_elapsed <= 84:
            self.set_ghost_mode(Mode.SCATTER)
        else:
            self.set_ghost_mode(Mode.CHASE)

    def set_ghost_mode(self, mode):
        if Ghost.mode != mode:
            Ghost.mode = mode
            for ghost in self.ghosts.values():
                ghost.reverse_direction()
    
    def release_ghost_from_prison(self, next_ghost):
        if next_ghost.pellet_count >= next_ghost.pellet_max:
            (next_ghost.x, next_ghost.y) = GHOST_LEAVE_POS
            next_ghost.prison = False
            next_ghost.next_dir = Direction.DOWN
            return True
        else:
            return False
