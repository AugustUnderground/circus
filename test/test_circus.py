""" Circus Test Suite """

import os
from collections import OrderedDict
import gym
from gym import GoalEnv
from stable_baselines3.common.vec_env.base_vec_env import VecEnv
import numpy as np

import circus

HOME = os.path.expanduser('~')

def _test_goal_env(env: GoalEnv):
    assert isinstance(env, VecEnv), \
           'The env must inherit from VecEnv.'
    assert isinstance(env, GoalEnv), \
           'The env must inherit from gym.GoalEnv.'

    assert hasattr(env, 'observation_space'), \
           'The env must specify an observation_space attribute.'
    assert hasattr(env, 'action_space'), \
           'The env must specify an action_space attribute.'

    assert isinstance(env.observation_space, gym.spaces.Dict), \
           'The observation_space must be of type gym.spaces.Dict.'
    assert isinstance(env.action_space, gym.spaces.Box), \
           'The action_space must be of type gym.spaces.Box.'

    assert ( sorted(env.observation_space.keys()) ==
             sorted(['achieved_goal', 'desired_goal', 'observation'])), \
           f'The observation space dict must contain ["achieved_goal", "desired_goal", "observation"] instead of {env.observation_space.keys()}.'

    assert np.any(np.abs(env.action_space.low) == np.abs(env.action_space.high)), \
           'The action space should be symmetric.'

    assert (np.any(np.abs(env.action_space.low)  >= 1.0) or \
            np.any(np.abs(env.action_space.high) >= 1.0)),  \
           'The action space is not ∈ [-1;1]'

    assert env.action_space.is_bounded(), \
           'The action space should be bounded.'

    obs = env.reset()

    assert isinstance(obs, OrderedDict), \
           'The observation returned by `reset` must be an OrderedDict array.'

    assert env.observation_space['observation'].shape[0] == obs['observation'].shape[1], \
           'The observation returned by `reset` ({obs["observation"].shape[1]}) does not match the given space ({env.observation_space["observation"].shape[0]}).'

    assert isinstance(obs['observation'], np.ndarray), \
           'The "observation" field must be a numpy array.'

    assert isinstance(obs['desired_goal'], np.ndarray), \
           'The "desired_goal" field must be a numpy array.'

    assert isinstance(obs['achieved_goal'], np.ndarray), \
           'The "achieved_goal" field must be a numpy array.'

    assert env.num_envs == obs['observation'].shape[0], \
           f'Number of Environments {env.num_envs} must align with first dimension of observations {obs["observation"].shape[0]}'

    assert obs['achieved_goal'].shape == obs['desired_goal'].shape, \
           f'Shape of achieved goal ({obs["achieved_goal"].shape}) does not match shape of desired goal ({obs["desired_goal"].shape}).'

    assert env.num_envs == obs['achieved_goal'].shape[0], \
           f'Number of Environments {env.num_envs} must align with first dimension of achieved_goal {obs["achieved_goal"].shape[0]}'

    assert env.num_envs == obs['desired_goal'].shape[0], \
           f'Number of Environments {env.num_envs} must align with first dimension of desired goal {obs["desired_goal"].shape[0]}'

    act = np.stack([env.action_space.sample()] * env.num_envs)

    assert all([env.action_space.shape[0] == a.shape[0] for a in act]), \
           f'The dimensions of the action ({env.action_space.shape[0]}) space do not match ({act.shape[1]}).'

    res = env.step(act)

    assert len(res) == 4, \
           f'The `step` function must return a tuple with four elements, not {len(res)}.'

    o,r,d,i = res

    assert isinstance(o, OrderedDict), \
           'The observation returned by `step` must be a numpy array.'

    assert isinstance(o['observation'], np.ndarray), \
           'The "observation" field must be a numpy array.'

    assert isinstance(o['desired_goal'], np.ndarray), \
           'The "desired_goal" field must be a numpy array.'

    assert isinstance(o['achieved_goal'], np.ndarray), \
           'The "achieved_goal" field must be a numpy array.'

    assert env.observation_space['observation'].shape[0] == o['observation'].shape[1], \
           'The observation returned by `reset` ({o["observation"].shape[1]}) does not match the given space ({env.observation_space["observation"].shape[0]}).'

    assert env.num_envs == o['observation'].shape[0], \
           f'Number of Environments {env.num_envs} must align with first dimension of observations {o["observation"].shape[0]}'

    assert o['achieved_goal'].shape == o['desired_goal'].shape, \
           f'Shape of achieved goal ({o["achieved_goal"].shape}) does not match shape of desired goal ({o["desired_goal"].shape}).'

    assert env.num_envs == o['achieved_goal'].shape[0], \
           f'Number of Environments {env.num_envs} must align with first dimension of achieved_goal {o["achieved_goal"].shape[0]}'

    assert env.num_envs == o['desired_goal'].shape[0], \
           f'Number of Environments {env.num_envs} must align with first dimension of desired goal {o["desired_goal"].shape[0]}'

    assert isinstance(r, np.ndarray), \
           'The reward returned by `step` must be of type np.array.'

    assert env.num_envs == r.shape[0], \
           f'Number of Environments {env.num_envs} must align with shape of reward {r.shape[0]}'

    assert isinstance(d, np.ndarray), \
           'The done signal returned by `step` must be of type np.array.'

    assert env.num_envs == d.shape[0], \
           f'Number of Environments {env.num_envs} must align with shape of done {d.shape[0]}'

    for _ in range(10):
        act = np.stack([env.action_space.sample()] * env.num_envs)
        obs, rew, don, inf = env.step(act)

        assert not np.any(np.isnan(obs['observation'])), \
               'Observations contain NaNs.'
        assert not np.any(np.isinf(obs['observation'])), \
               'Observations contain +/-Infs.'
        assert not np.any(np.isnan(obs['achieved_goal'])), \
               'Observations contain NaNs.'
        assert not np.any(np.isinf(obs['achieved_goal'])), \
               'Observations contain +/-Infs.'
        assert not np.any(np.isnan(obs['desired_goal'])), \
               'Observations contain NaNs.'
        assert not np.any(np.isinf(obs['desired_goal'])), \
               'Observations contain +/-Infs.'

def _test_vec_env(env: VecEnv):
    assert isinstance(env, VecEnv), \
           'The env must inherit from VecEnv.'

    assert hasattr(env, 'observation_space'), \
           'The env must specify an observation_space attribute.'
    assert hasattr(env, 'action_space'), \
           'The env must specify an action_space attribute.'

    assert isinstance(env.observation_space, gym.spaces.Box), \
           'The observation_space must be of type gym.spaces.Dict.'
    assert isinstance(env.action_space, gym.spaces.Box), \
           'The action_space must be of type gym.spaces.Box.'

    assert np.any(np.abs(env.action_space.low) == np.abs(env.action_space.high)), \
           'The action space should be symmetric.'

    assert (np.any(np.abs(env.action_space.low)  >= 1.0) or \
            np.any(np.abs(env.action_space.high) >= 1.0)),  \
           'The action space is not ∈ [-1;1]'

    assert env.action_space.is_bounded(), \
           'The action space should be bounded.'

    obs = env.reset()

    assert isinstance(obs, np.ndarray), \
           'The observation returned by `reset` must be a numpy array.'

    assert env.observation_space.shape[0] == obs.shape[1], \
           'The observation returned by `reset` ({obs.shape[1]}) does not match the given space ({env.observation_space.shape[0]}).'

    assert env.num_envs == obs.shape[0], \
           f'Number of Environments {env.num_envs} must align with first dimension of observations {obs.shape[0]}.'

    act = env.action_space.sample()

    assert env.action_space.shape[0] == act.shape[1], \
           f'The dimensions of the action ({env.action_space.shape[0]}) space do not match ({act.shape[1]}).'

    assert env.num_envs == act.shape[0], \
           f'Number of Environments {env.num_envs} must align with first dimension of actions {act.shape[0]}'

    res = env.step(act)

    assert len(res) == 4, \
           f'The `step` function must return a tuple with four elements, not {len(res)}.'

    o,r,d,i = res

    assert isinstance(o, np.ndarray), \
           'The observation returned by `step` must be a numpy array.'

    assert env.observation_space.shape[0] == o.shape[1], \
           'The observation returned by `reset` ({o.shape[1]}) does not match the given space ({env.observation_space.shape[0]}).'

    assert env.num_envs == o.shape[0], \
           f'Number of Environments {env.num_envs} must align with first dimension of observations {o.shape[0]}'

    assert isinstance(r, np.ndarray), \
           'The reward returned by `step` must be of type np.array.'

    assert env.num_envs == r.shape[0], \
           f'Number of Environments {env.num_envs} must align with shape of reward {r.shape[0]}'

    assert isinstance(d, np.ndarray), \
           'The done signal returned by `step` must be of type np.array.'

    assert env.num_envs == d.shape[0], \
           f'Number of Environments {env.num_envs} must align with shape of done {d.shape[0]}'

    for _ in range(10):
        act = env.action_space.sample()
        obs, rew, don, inf = env.step(act)

        assert not np.any(np.isnan(obs)), \
               'Observations contain NaNs.'
        assert not np.any(np.isinf(obs)), \
               'Observations contain +/-Infs.'

def _test_op_v0(env_id):
    env = circus.make(env_id, n_envs = 5)
    _test_goal_env(env)
    env.close()
    del env

def _test_op_v1(env_id):
    env = circus.make(env_id, n_envs = 5)
    _test_vec_env(env)
    env.close()
    del env

def test_op1_xh035_geom_v0():
    _test_op_v0('circus:op1-xh035-geom-v0')

def test_op2_xh035_geom_v0():
    _test_op_v0('circus:op2-xh035-geom-v0')

def test_op8_xh035_geom_v0():
    _test_op_v0('circus:op8-xh035-geom-v0')

def test_op1_xh035_elec_v0():
    _test_op_v0('circus:op1-xh035-elec-v0')

def test_op2_xh035_elec_v0():
    _test_op_v0('circus:op2-xh035-elec-v0')

def test_op8_xh035_elec_v0():
    _test_op_v0('circus:op8-xh035-elec-v0')

def test_op1_xh018_geom_v0():
    _test_op_v0('circus:op1-xh018-geom-v0')

def test_op2_xh018_geom_v0():
    _test_op_v0('circus:op2-xh018-geom-v0')

def test_op8_xh018_geom_v0():
    _test_op_v0('circus:op8-xh018-geom-v0')

def test_op1_xh018_elec_v0():
    _test_op_v0('circus:op1-xh018-elec-v0')

def test_op2_xh018_elec_v0():
    _test_op_v0('circus:op2-xh018-elec-v0')

def test_op8_xh018_elec_v0():
    _test_op_v0('circus:op8-xh018-elec-v0')
