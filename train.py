import os
import argparse
import gymnasium as gym
from datetime import datetime
from environment import PacmanEnv
#from src.utils import load_experiment, load_model, parse_bool
#from stable_baselines3.common.env_checker import check_env
#from stable_baselines3.common.policies import MlPPolicy
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3 import PPO, DQN, A2C

if __name__ == "__main__":
    # Create a new Reverse Pacman Environment
    env = PacmanEnv(render_mode='human')
    
    print("==================DEBUG==================\n", env.observation_space, "\n==================DEBUG==================\n")

    if not os.path.exists('logs'):
        os.makedirs('logs')

    # AGENT SETUP
    model = A2C("MultiInputPolicy", env, verbose=1, tensorboard_log='logs')

    # Training Logic
    start_time = datetime.now()
    print(f'Training started on {start_time.ctime()}')
    model.learn(total_timesteps=1_000_000)
    end_time = datetime.now()
    print(f'Training ended on {end_time.ctime()}')
    print(f'Training lasted {end_time - start_time}')
    
    # Save model
    if not os.path.exists('trained_models'):
        os.makedirs('trained_models')
    model.save(f'trained_models/pacman_100k.zip')
    
    env.close()
