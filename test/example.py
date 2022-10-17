import time
import gym
import numpy as np
from stable_baselines3 import A2C, HerReplayBuffer, DDPG, DQN, SAC, TD3, PPO
import circus

env = gym.make('circus:fca-gpdk180-geom-v0')
env.reset()

## SINGLE GOAL ENV, gym registry
env     = gym.make('circus:sym-xh018-geom-v0')
obs     = env.reset()
act     = env.action_space.sample()
o,r,d,i = env.step(act)

## TD3 + HER
her = TD3( "MultiInputPolicy"
         , env
         , replay_buffer_class = HerReplayBuffer
         , replay_buffer_kwargs = dict( n_sampled_goal = 4
                                      , goal_selection_strategy = 'future'
                                      , online_sampling = True
                                      , max_episode_length = 10
                                      , )
         , verbose = 1
         , )

her.learn(total_timesteps=2, log_interval=1)

## VECTOR GOAL ENV, circus native
n       = 5
envs    = circus.make('circus:sym-xh018-elec-v0', n_envs = n)
obs     = envs.reset()
act     = np.vstack([envs.action_space.sample() for _ in range(n)])

for t in range(10):
    act     = np.vstack([envs.action_space.sample() for _ in range(n)])
    tic     = time.time()
    o,r,d,i = envs.step(act)
    toc     = time.time()
    delta   = toc - tic
    print(f'({t}) Took: {delta:.3}s')

a2c     = A2C("MlpPolicy", envs, verbose=1)
a2c.learn(total_timesteps=2, log_interval=1)
