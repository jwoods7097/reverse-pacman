import gymnasium as gym

import game

if __name__ == '__main__':
    env = gym.make("PacMan-v0", render_mode="human")
    env.reset()

    for i in range(1000):
        env.step(env.action_space.sample())

