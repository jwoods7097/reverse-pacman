import numpy as np
import pygame

import gymnasium as gym
from gymnasium import spaces
from gymnasium.envs.registration import register

from globals import LEVEL_HEIGHT, LEVEL_WIDTH, TILE_PIXEL_SIZE
from level import Level, Tile
from pacman import Pacman
from ghost import Blinky
from entity import Direction
import utils

register(
    id="PacMan-v0",
    entry_point="game:PacmanEnv",
)

class PacmanEnv(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 4}

    def __init__(self, render_mode=None):
        
        # Encodes data about pacman's location, the ghosts' location, and the level state
        self.observation_space = spaces.Dict(
            {
                # for entities, we are storing (x, y, v_x, v_y)
                "pacman": spaces.Box(np.array([0, 0, -1, -1]), np.array([LEVEL_WIDTH, LEVEL_HEIGHT, 1, 1]), dtype=np.float32),
                "blinky": spaces.Box(np.array([0, 0, -1, -1]), np.array([LEVEL_WIDTH, LEVEL_HEIGHT, 1, 1]), dtype=np.float32),
                "inky":   spaces.Box(np.array([0, 0, -1, -1]), np.array([LEVEL_WIDTH, LEVEL_HEIGHT, 1, 1]), dtype=np.float32),
                "pinky":  spaces.Box(np.array([0, 0, -1, -1]), np.array([LEVEL_WIDTH, LEVEL_HEIGHT, 1, 1]), dtype=np.float32),
                "clyde":  spaces.Box(np.array([0, 0, -1, -1]), np.array([LEVEL_WIDTH, LEVEL_HEIGHT, 1, 1]), dtype=np.float32),
                "level":  spaces.MultiBinary([LEVEL_WIDTH, LEVEL_HEIGHT, len(Tile)])
            }
        )

        # The 5 actions are: no-op, left, up, right, down
        self.action_space = spaces.Discrete(5)

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

        # Pygame objects
        self.window = None
        self.clock = None

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
        self.ghosts = [Blinky(13, 14)]
        
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
        if direction != Direction.NONE:
            self.pacman.turn(direction)

        # Punish Pacman a bit for not eating pellets
        reward = -1
        terminated = False

        # Pacman movement
        if self.pacman.can_move(self.level):
            self.pacman.move()
            reward = self.pacman.eat(self.level[self.pacman.y, self.pacman.x])
            self.level[self.pacman.y, self.pacman.x] = Tile.EMPTY

        # Ghost movement
        for ghost in self.ghosts:
            ghost.set_dir(self.level, self.pacman.x, self.pacman.y)
            ghost.move()

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

        # Update display
        pygame.event.pump()
        pygame.display.update()
        self.clock.tick(self.metadata["render_fps"])

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()
