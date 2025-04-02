import os
import argparse
from datetime import datetime
from game import ReversePacman
from src.utils import load_experiment, load_model, parse_bool
from stable_baselines3.common.env_checker import check_env
from stable_baselines.common.policies import MlPPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import DQN





if __name__ == "__main__":
    """ALGO PARAMS"""
    #parse arguments
    """parser = argparse.ArgumentParser()

    parser.add_argument('--algorithm', type=str, required=True, help='The DRL algorithm to use')
    parser.add_argument('--set', required=True, type=int, help='The experiment set to use, from the sets defined in the experiments directory')
    parser.add_argument('--resume', type=parse_bool, default=False, help='If true, loads an existing model to resume trianing. If false, trains a new model')
    
    args = parser.parse_args()
    print(f'Algorithm: {args.algorithm} \nSet: {args.set}\nGamma: {args.gamma}\nTraining steps: {args.steps}\n')"""
    
    """if args.resume:
        model = load_model(args.algorithm, args.set)
        model.set_env(env)
    else:
        if args.algorithm == 'DQN':"""
    
    """ENV SETUP"""
    # Create a new Reverse Pacman Environment
    env = ReversePacman()

    if not os.path.exists('logs'):
        os.makedirs('logs')

    """AGENT SETUP"""
    model = DQN(MlPPolicy, env, verbose=1)

    """Training Logic"""
    start_time = datetime.now()
    print(f'Training started on {start_time.ctime()}')
    model.learn()
    end_time = datetime.now()
    print(f'Training ended on {end_time.ctime()}')
    print(f'Training lasted {end_time - start_time}')

