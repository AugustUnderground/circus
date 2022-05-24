import gym
from stable_baselines3 import A2C, HerReplayBuffer, DDPG, DQN, SAC, TD3, PPO
import circus

## SINGLE ENV

#env = gym.make('circus:op2-xh035-geom-v0')
env = circus.make_vec_env('circus:op2-xh035-geom-v0', n_envs=1)

ddpg = DDPG('MlpPolicy', env, verbose = 1)
ddpg.learn(total_timesteps=2, log_interval=1)

## VECTOR ENV

envs = circus.make_vec_env('circus:op2-xh035-geom-v0', n_envs=5)

a2c = A2C("MlpPolicy", envs, verbose=1)
a2c.learn(total_timesteps=2, log_interval=1)

## GOAL ENV

genv = circus.make_goal_env('circus:op2-xh035-geom-v0', n_envs=1)

her = TD3("MultiInputPolicy", genv , replay_buffer_class = HerReplayBuffer , replay_buffer_kwargs = dict( n_sampled_goal = 4 , goal_selection_strategy = 'future' , online_sampling = True , max_episode_length = 10 , ) , verbose = 1 , )

her.learn(total_timesteps=10, log_interval=1)
