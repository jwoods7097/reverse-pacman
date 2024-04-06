import gymnasium as gym

import game

if __name__ == '__main__':
    env = gym.make("PacMan-v0", render_mode="human")
    env.reset()

    for i in range(1000):
        observation, reward, terminated, truncated, info = env.step(env.action_space.sample())
        if i % 10 == 0:
            print(i, info['score'])

