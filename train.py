import gymnasium as gym
from game import PacmanEnv
from stable_baselines3.common.env_checker import check_env
from stable_baselines.common.policies import MlPPolicy
#from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import PPO, DQN

#import game

if __name__ == '__main__':
    """"env = gym.make("PacMan-v0", render_mode="human")
    env.reset()

    for i in range(1000):
        observation, reward, terminated, truncated, info = env.step(env.action_space.sample())
        if i % 10 == 0:
            print(i, info['score'])"""
    
    """ALGO PARAMS"""
    learning_rate = ""
    batch_size = ""
    
    """ENV SETUP"""
    # Create a new Reverse Pacman Environment
    env = PacmanEnv()

    """AGENT SETUP"""
    model = PPO(MlPPolicy, env, verbose=1)
    model = DQN(MlPPolicy, env, verbose=1)

    """Training Logic"""
    model.learn()

