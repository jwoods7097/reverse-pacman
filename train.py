import os
import argparse
from datetime import datetime
from game import PacmanEnv
#from src.utils import load_experiment, load_model, parse_bool
#from stable_baselines3.common.env_checker import check_env
#from stable_baselines3.common.policies import MlPPolicy
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3 import DQN





if __name__ == "__main__":
    """ALGO PARAMS"""
    
    """ENV SETUP"""
    # Create a new Reverse Pacman Environment
    env = PacmanEnv()
    
    print("==================DEBUG==================\n", env.observation_space, "\n==================DEBUG==================\n")

    if not os.path.exists('logs'):
        os.makedirs('logs')

    """AGENT SETUP"""
    model = DQN("MultiInputPolicy", env, verbose=1)

    """Training Logic"""
    start_time = datetime.now()
    print(f'Training started on {start_time.ctime()}')
    model.learn(total_timesteps=100)
    end_time = datetime.now()
    print(f'Training ended on {end_time.ctime()}')
    print(f'Training lasted {end_time - start_time}')

