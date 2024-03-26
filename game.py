import numpy as np
import pygame

import gymnasium as gym
from gymnasium import spaces
from gymnasium.envs.registration import register

from globals import LEVEL_HEIGHT, LEVEL_WIDTH
from level import Level, Tile
from pacman import Pacman

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
        pass

    def _get_info(self):
        pass

    def reset(self, seed=None, options=None):
        # We need the following line to seed self.np_random
        super().reset(seed=seed)

        # Game objects
        self.pacman = Pacman(13, 26)
        
        self.level = Level('assets/levels/level1.txt')

        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation, info

    def step(self, action):
        


        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation, reward, terminated, False, info
    
    def render(self):
        if self.render_mode == "human":
            return self._render_frame()
        
    def _render_frame(self):
        pass

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()
