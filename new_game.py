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
from pacman import Pacman
from spritesheet import Spritesheet



register(
    id="PacMan-v0",
    entry_point="game:PacmanEnv",
)

class PacmanEnv(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 4}

    def __init__(self, render_mode=None):
        
        # Encodes data about pacman's location, the ghosts' location, and the level state
        """self.observation_space = spaces.Dict(
            {
                # for entities, we are storing (x, y, v_x, v_y)
                "pacman": spaces.Box(np.array([0, 0, -1, -1]), np.array([LEVEL_WIDTH, LEVEL_HEIGHT, 1, 1]), dtype=np.float32),
                "blinky": spaces.Box(np.array([0, 0, -1, -1]), np.array([LEVEL_WIDTH, LEVEL_HEIGHT, 1, 1]), dtype=np.float32),
                "inky":   spaces.Box(np.array([0, 0, -1, -1]), np.array([LEVEL_WIDTH, LEVEL_HEIGHT, 1, 1]), dtype=np.float32),
                "pinky":  spaces.Box(np.array([0, 0, -1, -1]), np.array([LEVEL_WIDTH, LEVEL_HEIGHT, 1, 1]), dtype=np.float32),
                "clyde":  spaces.Box(np.array([0, 0, -1, -1]), np.array([LEVEL_WIDTH, LEVEL_HEIGHT, 1, 1]), dtype=np.float32),
                "level":  spaces.MultiBinary([LEVEL_WIDTH, LEVEL_HEIGHT, len(Tile)])
            }
        )"""
        self.level = Level('assets/levels/level1.txt')

        self.observation_space = spaces.Dict(
            {
                # Initializing each entity in the game
                "pacman": Pacman(13, 26)
            }
        )

        self.ghosts = spaces.Dict(
            {
                "blinky": Blinky(13, 14),
                "clyde": Clyde(13, 16),
                "inky": Inky(14, 16),
                "pinky": Pinky(15, 16)
            }
        )

        # The 5 actions are: no-op, left, up, right, down
        self.action_space = spaces.Discrete(5)

        sprite_sheet = Spritesheet("assets/sprites/pacman_sprites.png")
        ghost_fruit_sprite_sheet = Spritesheet("assets/sprites/ghost_fruit_sprites.png")
        base_state = sprite_sheet.parse_sprite("pacman_s.png")
        pacman_image_data = {d: [base_state] for d in Direction}
        ghost_image_data = {ghost: {d: [] for d in Direction} for ghost in ghosts}

        for i in range(2):
            for d in Direction:
                pacman_image_data[d].append(sprite_sheet.parse_sprite(f"pacman_{d.value}{i+1}.png"))

        for name in self.ghosts:
            for d in Direction:
                ghost_image_data[name][d].append(ghost_fruit_sprite_sheet.parse_sprite(f"{name}_{d.value}{i + 1}.png"))

        cherry = ghost_fruit_sprite_sheet.parse_sprite("cherry.png")

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

        # Pygame objects
        pygame.init()
        self.window = pygame.display.set_mode((LEVEL_WIDTH*TILE_PIXEL_SIZE, LEVEL_HEIGHT*TILE_PIXEL_SIZE))
        self.clock = pygame.time.Clock("Reverse Pacman")
        self.font = pygame.font.Font('assets/fonts/emulogic.ttf', 10)

    def _get_obs(self):  
        level_obs = np.zeros_like(self.level.board, dtype=object)
        for y, row in enumerate(self.level.board):
            for x, tile in enumerate(row):
                arr = np.zeros(len(Tile), dtype=bool)
                arr[tile.value] = True
                level_obs[y, x] = arr

        return {
                # for entities, we are storing (x, y, v_x, v_y)
                "pacman": [self.pacman.x, self.pacman.y, *self.pacman.get_velocity()],
                "blinky": [self.ghosts[0].x, self.ghosts[0].y, *self.ghosts[0].get_velocity()],
                "inky":   [0,0,0,0],
                "pinky":  [0,0,0,0],
                "clyde":  [0,0,0,0],
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
        self.pacman = Pacman(13, 26)

        self.blinky = Blinky(13, 14)
        self.clyde = Clyde(13,16)
        self.inky = Inky(14,16)
        self.pinky = Pinky(15,16)
        
        self.level = Level('assets/levels/level1.txt')

        self.episode_step = 0

        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

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

        # if we release a ghost, then we have to know what ghost to release next
        # the first one we will always release is pinky, then inky, then clyde
        if next_ghost_out.prison and self.release_ghost_from_prison(next_ghost_out):
            if self.pinky.prison: next_ghost_out = self.pinky
            elif self.inky.prison: next_ghost_out = self.inky
            elif self.clyde.prison: next_ghost_out = self.clyde

        # Pacman movement
        if self.pacman.can_move(self.level):
            self.pacman.move()
            reward = self.pacman.eat(self.level[self.pacman.y, self.pacman.x])
            self.level[self.pacman.y, self.pacman.x] = Tile.EMPTY
            
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
            pygame.display.set_caption("Pacman")
            self.window = pygame.display.set_mode((LEVEL_WIDTH*TILE_PIXEL_SIZE, LEVEL_HEIGHT*TILE_PIXEL_SIZE))
        if self.clock is None and self.render_mode == "human":
            self.clock = pygame.time.Clock()
        if self.font is None and self.render_mode == "human":
            self.font = pygame.font.Font('assets/fonts/emulogic.ttf', 10)

        # Draw background
        self.window.fill("black")

        # Draw level
        for y, row in enumerate(self.level.board):
            for x, tile in enumerate(row):
                if tile == Tile.WALL:
                    pygame.draw.rect(self.window, "blue", utils.square(x,y,TILE_PIXEL_SIZE))
                elif tile == Tile.PELLET:
                    pygame.draw.circle(self.window, "white", *utils.circle(x,y,TILE_PIXEL_SIZE/5))
                elif tile == Tile.POWER_PELLET:
                    pygame.draw.circle(self.window, "white", *utils.circle(x,y,2*TILE_PIXEL_SIZE/5))

        # Draw pacman
        pygame.draw.circle(self.window, "yellow", *utils.circle(self.pacman.x,self.pacman.y,TILE_PIXEL_SIZE/2))

        # Draw ghosts
        for ghost in self.ghosts:
            color = "red"
            pygame.draw.circle(self.window, color, *utils.circle(ghost.x,ghost.y,TILE_PIXEL_SIZE/2))

        # Draw text
        score_text = self.font.render(f'Score: {self.pacman.score}', True, 'white')
        self.window.blit(score_text, (0, 0))
        step_text = self.font.render(f'Step: {self.episode_step}', True, 'white')
        self.window.blit(step_text, (0, 12))
        
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
        time_elapsed = tick_counter / FPS
        if time_elapsed <= 7:
            self.set_ghost_mode(Mode.SCATTER)
        elif time_elapsed <= 27:
            self.set_ghost_mode(Mode.CHASE)
        elif time_elapsed <= 34:
            self.set_ghost_mode(Mode.SCATTER)
        elif time_elapsed <= 54:
            self.set_ghost_mode(Mode.CHASE)
        elif time_elapsed <= 59:
            self.set_ghost_mode(Mode.SCATTER)
        elif time_elapsed <= 79:
            self.set_ghost_mode(Mode.CHASE)
        elif time_elapsed <= 84:
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