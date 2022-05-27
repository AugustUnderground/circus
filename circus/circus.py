"""Circus"""

import os
from functools import partial
from collections import OrderedDict
from typing import Any, List, Optional, Type, Union, Callable
import gym
from gym.spaces import Dict, Box
from gym import GoalEnv
from stable_baselines3.common.vec_env.base_vec_env import VecEnv, \
                                                          VecEnvIndices, \
                                                          VecEnvStepReturn

import numpy as np
import hace as ac

from .util   import *
from .reward import *
from .ace    import *
from .prim   import *
from .trafo  import *

class CircusGeom(GoalEnv, VecEnv):
    """ Geometric Sizing Goal Environment """
    def __init__( self
                , ace_id: str
                , ace_backend: str
                , num_envs: int          = 1
                , num_steps: int         = 50
                , seed: int              = 666
                , goal_ids: [str]        = []
                , goal_preds: [Callable] = []
                , reward_fn: Callable    = binary_reward
                , ):

        self.ace_id: str       = ace_id
        self.ace_backend: str  = ace_backend
        self.num_envs: int     = num_envs

        self.num_steps: int    = num_steps
        self.steps: np.array   = np.zeros(num_envs)

        self.calculate_reward  = reward_fn

        self.ace_envs          = ac.make_same_env_pool( self.num_envs
                                                      , self.ace_id
                                                      , self.ace_backend )

        performance_ids        = sorted(ac.performance_identifiers(self.ace_envs[0]))
        sizing_ids             = len(ac.sizing_identifiers(self.ace_envs[0]))

        self.goal_ids          = goal_ids or [ident for ident in performance_ids
                                                    if ident.islower() or (ident == 'A')]

        self.goal_idx          = np.array([i for i,p in enumerate(performance_ids)
                                             if p in self.goal_ids])

        self.goal_preds        = goal_preds or goal_predicate(self.goal_ids)

        self.action_space      = Box( low   = -1.0
                                    , high  = 1.0
                                    , shape = (sizing_ids,)
                                    , dtype = np.float32 )

        self.observation_space = Dict({ 'observation':  Box( -np.Inf, np.Inf
                                                           , (len(performance_ids),))
                                      , 'achieved_goal': Box( -np.Inf, np.Inf
                                                            , (len(self.goal_ids),))
                                      , 'desired_goal':  Box( -np.Inf, np.Inf
                                                            , (len(self.goal_ids),))
                                      , })

        self.rng_seed          = seed

        pool                   = { i: self.ace_envs[i]
                                   for i in range(self.num_envs) }
        initial_sizing         = ac.initial_sizing_pool(pool)
        results                = ac.evaluate_circuit_pool(pool, pool_params = initial_sizing)
        self.reference_goal    = np.array([ [ p for k,p in r.items() if k in self.goal_ids]
                                                for r in results.values() ])
        self.goal              = add_noise(self.reference_goal)

        self.constraints       = ac.parameter_dict(self.ace_envs[0])

        self.unscale_action    = geometric_unscaler(self.constraints)

        self.sizing            = {}

        VecEnv.__init__( self, self.num_envs
                       , self.observation_space
                       , self.action_space )

    def close(self) -> None:
        for _,env in self.ace_envs.items():
            env.clear()

    def reset(self, env_mask: [bool] = [], env_ids: [int] = []):
        reset_ids     = [ i for i,m in enumerate(env_mask) if m
                        ] or env_ids or range(self.num_envs)
        pool          = { i: self.ace_envs[i] for i in reset_ids }
        random_sizing = ac.random_sizing_pool(pool)
        results       = ac.evaluate_circuit_pool(pool, pool_params = random_sizing)
        state         = np.vstack([ np.array([ p for _,p in
                                               sorted( results[i].items()
                                                     , key = lambda kv: kv[0])])
                                    for i in range(len(results)) ])
        self.goal     = add_noise(self.reference_goal)
        achieved      = ( state[:,self.goal_idx]
                        if (len(state.shape) > 1)
                        else state[self.goal_idx] )
        observation   = OrderedDict({ 'observation': state
                                    , 'achieved_goal': achieved
                                    , 'desired_goal': self.goal })

        self.steps[reset_ids] = 0

        return observation

    def step(self, actions: np.ndarray) -> VecEnvStepReturn:
        self.step_async(actions)
        return self.step_wait()

    def step_async(self, actions: np.ndarray) -> None:
        unscaled    = list(self.unscale_action(actions))
        params      = sorted(ac.sizing_identifiers(self.ace_envs[0]))
        self.sizing = { env_id: dict(zip(params, action.tolist()))
                        for env_id,action in enumerate(unscaled)}

    def step_wait(self) -> VecEnvStepReturn:
        pool        = { i: self.ace_envs[i]
                        for i in range(self.num_envs) }
        results     = ac.evaluate_circuit_pool(pool, pool_params = self.sizing)

        obs         = np.vstack([ np.array([ p for _,p in
                                             sorted( results[i].items()
                                                   , key = lambda kv: kv[0]) ])
                                  for i in range(len(results)) ])
        achieved    = ( obs[:,self.goal_idx] if (len(obs.shape) > 1)
                                             else obs[self.goal_idx] )
        observation = OrderedDict({ 'observation': obs
                                  , 'achieved_goal': achieved
                                  , 'desired_goal': self.goal })

        reward      = self.calculate_reward(self.goal_preds, self.goal, achieved)

        self.steps  = self.steps + 1

        done        = (reward == 0) | (self.steps >= self.num_steps)

        info        = [{ 'outputs': sorted(list(results[0].keys()))
                       , 'goal': self.goal_ids
                       , 'inputs':  sorted(ac.sizing_identifiers(self.ace_envs[0]))
                       , }] * self.num_envs

        return (observation, reward, done, info)

    def get_attr( self, attr_name: str, indices: VecEnvIndices = None
                ) -> List[Any]:
        target_envs = self._get_target_envs(indices)
        return [getattr(env_i, attr_name) for env_i in target_envs]

    def set_attr( self, attr_name: str, value: Any
                , indices: VecEnvIndices = None) -> None:
        target_envs = self._get_target_envs(indices)
        for env_i in target_envs:
            setattr(env_i, attr_name, value)

    def env_method( self, method_name: str, *method_args
                  , indices: VecEnvIndices = None, **method_kwargs
                  ) -> List[Any]:
        target_envs = self._get_target_envs(indices)
        return [ getattr(env_i, method_name)(*method_args, **method_kwargs)
                 for env_i in target_envs ]

    def env_is_wrapped( self, wrapper_class: Type[gym.Wrapper]
                      , indices: VecEnvIndices = None) -> List[bool]:
        return [False for _ in range(self.num_envs)]

    def _get_target_envs(self, indices: VecEnvIndices) -> List[gym.Env]:
        return [self]

    def seed(self, seed: Optional[int] = None) -> List[Union[None, int]]:
        self.rng_seed = seed
        return [self.rng_seed] * self.num_envs

    def render(self, mode: str = 'human') -> Optional[np.ndarray]:
        pass

class CircusElec(CircusGeom):
    """ Electric Sizing Goal Environment """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        nmos_path = os.path.expanduser(f'~/.ace/{self.ace_backend}/nmos')
        pmos_path = os.path.expanduser(f'~/.ace/{self.ace_backend}/pmos')
        params_x  = ['gmoverid', 'fug', 'Vds', 'Vbs']
        params_y  = ['idoverw', 'L', 'gdsoverw', 'Vgs']
        trafo_x   = ['fug']
        trafo_y   = ['idoverw', 'gdsoverw']
        self.nmos = PrimitiveDevice(nmos_path, params_x, params_y, trafo_x, trafo_y)
        self.pmos = PrimitiveDevice(pmos_path, params_x, params_y, trafo_x, trafo_y)

        self.transformation = partial( transformation(self.ace_id)
                                     , self.constraints
                                     , self.nmos
                                     , self.pmos
                                     , )

        electric_ids      = len(electric_identifiers(self.ace_id))
        self.action_space = Box( low   = -1.0
                               , high  = 1.0
                               , shape = (electric_ids,)
                               , dtype = np.float32 )

        self.unscale_action = electric_unscaler(self.ace_id, self.ace_backend)

    def step_async(self, actions: np.ndarray) -> None:
        unscaled    = list(self.unscale_action(actions))
        self.sizing = { env_id: self.transformation(* action.flatten().tolist())
                        for env_id,action in enumerate(unscaled) }

class CircusGeomVec(CircusGeom):
    """ Geometric Sizing Non-Goal Environment """
    def __init__(self, reward_fn: Callable = default_reward, **kwargs):
        super().__init__(**(kwargs | {'reward_fn': reward_fn}))
        self.observation_space = self.observation_space['observation']

    def reset(self, **kwargs) -> np.array:
        obs = super().reset(**kwargs)
        return obs['observation']

    def step_wait(self) -> VecEnvStepReturn:
        obs, _, done, info = super().step_wait()
        observation        = obs['observation']
        reward             = self.calculate_reward(observation)
        return (observation, reward, done, info)

class CircusElecVec(CircusElec):
    """ Geometric Sizing Non-Goal Environment """
    def __init__(self, reward_fn: Callable = default_reward, **kwargs):
        super().__init__(**(kwargs | {'reward_fn': reward_fn}))
        self.observation_space = self.observation_space['observation']

    def reset(self, **kwargs) -> np.array:
        obs = super().reset(**kwargs)
        return obs['observation']

    def step_wait(self) -> VecEnvStepReturn:
        obs, _, done, info = super().step_wait()
        observation        = obs['observation']
        reward             = self.calculate_reward(observation)
        return (observation, reward, done, info)

def make(env_id: str, n_envs: int = 1, **kwargs) -> Union[ CircusGeom
                                                         , CircusGeomVec ]:
    """ Gym Style Environment Constructor """
    id,pdk,space,var = env_id.split(':')[1].split('-')
    backend = backend_id(pdk)
    env     = ( CircusGeom( ace_id      = id
                          , ace_backend = backend
                          , num_envs    = n_envs
                          , **kwargs
                          )    if (var == 'v0' and space == 'geom') else
                CircusGeomVec( ace_id      = id
                             , ace_backend = backend
                             , num_envs    = n_envs
                             , **kwargs
                             ) if (var == 'v1' and space == 'geom') else
                CircusElec( ace_id      = id
                          , ace_backend = backend
                          , num_envs    = n_envs
                          , **kwargs
                          )    if (var == 'v0' and space == 'elec') else
                CircusElecVec( ace_id      = id
                             , ace_backend = backend
                             , num_envs    = n_envs
                             , **kwargs
                             ) if (var == 'v1' and space == 'elec') else
                NotImplementedError(f'Variant {var} not available') )
    return env
