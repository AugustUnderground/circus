import gym
import numpy as np
from stable_baselines3 import A2C, HerReplayBuffer, DDPG, DQN, SAC, TD3, PPO
import circus

## SINGLE GOAL ENV, gym registry
env     = gym.make('circus:op2-xh035-geom-v0')
obs     = env.reset()
a       = np.random.randn(env.action_space.shape[0])
o,r,d,i = env.step(a)

## SINGLE Non-GOAL ENV, gym registry
env     = gym.make('circus:op2-xh035-geom-v1')
obs     = env.reset()
a       = np.random.randn(env.action_space.shape[0])
o,r,d,i = env.step(a)

## SINGLE GOAL ENV, circus native
env = circus.make('circus:op2-xh035-geom-v0')

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

## SINGLE Non-GOAL ENV, circus native
env  = circus.make('circus:op2-xh035-geom-v1')
ddpg = DDPG('MlpPolicy', env, verbose = 1)
ddpg.learn(total_timesteps=2, log_interval=1)

## VECTOR Non-GOAL ENV, circus native
envs = circus.make('circus:op2-xh035-geom-v1', n_envs = 5)
a2c  = A2C("MlpPolicy", envs, verbose=1)
a2c.learn(total_timesteps=2, log_interval=1)

## Random Test
env     = circus.make('circus:op1-xh035-elec-v0', n_envs = 5)
obs     = env.reset()
a       = np.vstack([env.action_space.sample()] * 5)
o,r,d,i = env.step(a)



pp = [ pp for pp in ac.performance_identifiers(env.ace_envs[0]) if (pp.islower() or (pp == 'A')) ]

pf = ['a_0', 'ugbw', 'pm', 'voff_stat', 'cmrr', 'psrr_p', 'A']

pm = np.array([ (p in pf) for p in pp ])

p = np.random.rand(10,23)

p[:, pm]
