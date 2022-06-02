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
env     = circus.make('circus:op1-xh035-elec-v0', n_envs = 5, goal_init = 'random', goal_filter = ['a_0', 'ugbw'])
obs     = env.reset()
a       = np.vstack([env.action_space.sample()] * 5)
o,r,d,i = env.step(a)


a = {'A', 'a_0', 'cmrr', 'cof', 'gm', 'i_out_max', 'i_out_min', 'idd', 'iss', 'overshoot_f', 'overshoot_r', 'pm', 'psrr_n', 'psrr_p', 'sr_f', 'sr_r', 'ugbw', 'v_ih', 'v_il', 'v_oh', 'v_ol', 'voff_stat', 'voff_sys'}
b = { 'a_0', 'ugbw', 'pm', 'gm', 'sr_r', 'sr_f', 'vn_1Hz', 'vn_10Hz', 'vn_100Hz'    , 'vn_1kHz', 'vn_10kHz', 'vn_100kHz', 'cmrr', 'psrr_n', 'psrr_p', 'v_il'        , 'v_ih', 'v_ol', 'v_oh', 'i_out_min', 'i_out_max', 'overshoot_r' , 'overshoot_f', 'cof', 'voff_stat', 'voff_sys', 'A' }
