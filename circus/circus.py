""" Gym compatible Analog Circuit Environment """

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
                , num_envs: int                    = 1
                , num_steps: int                   = 50
                , seed: int                        = 666
                , obs_filter: Union[str,List[str]] = 'perf'
                , goal_filter: [str]               = None
                , goal_preds: [Callable]           = None
                , reward_fn: Callable              = None
                , scale_observation: bool          = True
                , ):
        """
        Construct a Geometric Sizing Goal Environment
        Arguments:
            `ace_id`:            ID of the form 'op#', see ACE Documentation for further
                                 details.
            `ace_backend`:       PDK, available are 'xh035' and 'xh018'.
            `num_envs`:          Numer of Parallel Environments ∈ [ 1 .. `nproc` ]
            `num_steps`:         Number of steps per Episode.
            `seed`:              Random Seed
            `obs_filter`:        Filter Performance dict obtained from ACE.
                                 'perf': Only performance paramters
                                 'all': All parameters from ACE
                                 [str]: List of parameters
            `goal_filter`:       List of parameters
            `goal_preds`:        Binary comparison operator
            `reward_fn`:         Optional reward function that takes an observation dict.
            `scale_observation`: Scale the observations and goals as specified in trafo
        """

        self.ace_id: str       = ace_id
        self.ace_backend: str  = ace_backend
        self.num_envs: int     = num_envs

        self.num_steps: int    = num_steps
        self.steps: np.array   = np.zeros(num_envs)

        self.ace_envs          = ac.make_same_env_pool( self.num_envs
                                                      , self.ace_id
                                                      , self.ace_backend )

        self.constraints       = ac.parameter_dict(self.ace_envs[0])

        perf_ids               = sorted(ac.performance_identifiers(self.ace_envs[0]))
        self.obs_filter        = ( perf_ids if obs_filter == 'all' else
                                   [p for p in perf_ids if (p.islower() or (p == 'A'))]
                                   if obs_filter == 'perf' else
                                   obs_filter if isinstance(obs_filter, list)
                                   else ValueError('Wrong Argument type passed to obs_filter.') )

        self.obs_idx           = np.array([ i for i,p in enumerate(self.obs_filter)
                                            if p in self.obs_filter ])

        self.obs_scaler,_      = performance_scaler( self.ace_id
                                                   , self.ace_backend
                                                   , self.constraints
                                                   , self.obs_filter
                                                   , )

        self.input_parameters  = ac.sizing_identifiers(self.ace_envs[0])

        self.goal_filter       = goal_filter or [ ident for ident in self.obs_filter
                                                  if ident.islower() or (ident == 'A') ]

        self.goal_idx          = np.array([i for i,p in enumerate(self.obs_filter)
                                             if p in self.goal_filter])

        self.goal_preds        = goal_preds or goal_predicate(self.goal_filter)

        self.goal_scaler,_     = performance_scaler( self.ace_id
                                                   , self.ace_backend
                                                   , self.constraints
                                                   , self.goal_filter
                                                   , )

        self.calculate_reward  = reward_fn or partial(binary_reward, self.goal_preds)

        self.action_space      = Box( low   = -1.0
                                    , high  = 1.0
                                    , shape = (len(self.input_parameters),)
                                    , dtype = np.float32 )

        self.observation_space = Dict({ 'observation':   Box( -np.Inf, np.Inf
                                                            , (len(self.obs_filter),))
                                      , 'achieved_goal': Box( -np.Inf, np.Inf
                                                            , (len(self.goal_filter),))
                                      , 'desired_goal':  Box( -np.Inf, np.Inf
                                                            , (len(self.goal_filter),))
                                      , })

        self.scale_observation = scale_observation

        self.rng_seed          = seed

        pool                   = { i: self.ace_envs[i]
                                   for i in range(self.num_envs) }
        initial_sizing         = ac.initial_sizing_pool(pool)
        results                = ac.evaluate_circuit_pool(pool, pool_params = initial_sizing)
        self.reference_goal    = filter_results(self.goal_filter, results)
        self.goal              = add_noise(self.reference_goal)

        self.unscale_action    = geometric_unscaler(self.constraints)

        self.sizing            = {}

        VecEnv.__init__( self, self.num_envs
                       , self.observation_space
                       , self.action_space )

    def close(self, env_ids: list[int] = None) -> None:
        """
        Close all (parallel) ACE environment(s).
        Arguments:
            `env_ids`: List of environemt IDs that will be closed.
                       Default = None closes all.
        """
        for env_id in (env_ids or self.ace_envs.keys()):
            self.ace_envs[env_id].clear()

    def reset(self, env_mask: [bool] = [], env_ids: [int] = []):
        """
        Reset all (parallel) environemt(s).
        Arguments:
            `env_mask`: Boolean mask of environemts that will be reset. Passing
                        the `done` vector works. (Presendece)
            `env_ids`: List of integer IDs of environemts that will be reset.
        """
        reset_ids     = [ i for i,m in enumerate(env_mask) if m
                        ] or env_ids or range(self.num_envs)
        pool          = { i: self.ace_envs[i] for i in reset_ids }
        random_sizing = ac.random_sizing_pool(pool)
        results       = ac.evaluate_circuit_pool(pool, pool_params = random_sizing)
        self.goal     = add_noise(self.reference_goal)
        state         = filter_results(self.obs_filter, results)
        achieved      = filter_results(self.goal_filter, results)
        observation   = OrderedDict({ 'observation':   ( self.obs_scaler(state)
                                                         if self.scale_observation
                                                         else state )
                                    , 'achieved_goal': ( self.goal_scaler(achieved)
                                                         if self.scale_observation
                                                         else achieved )
                                    , 'desired_goal':  ( self.goal_scaler(self.goal)
                                                         if self.scale_observation
                                                         else self.goal ) })

        self.steps[reset_ids] = 0

        return observation

    def step(self, actions: np.ndarray) -> VecEnvStepReturn:
        """
        Take a step in the Environment. Calls `step_async` and `step_wait`
        under the hood.
        Arguments:
            `actions`: Take Action with shape [num_envs, action_space].
        """
        self.step_async(actions)
        return self.step_wait()

    def step_async(self, actions: np.ndarray) -> None:
        """
        Initiate a step in the Environment. 
        Arguments:
            `actions`: Take Action with shape [num_envs, action_space].
        """
        unscaled    = list(self.unscale_action(actions))
        params      = sorted(ac.sizing_identifiers(self.ace_envs[0]))
        self.sizing = { env_id: dict(zip(params, action.tolist()))
                        for env_id,action in enumerate(unscaled)}

    def step_wait(self) -> VecEnvStepReturn:
        """
        Complete a step in the Environment.
        """
        pool        = { i: self.ace_envs[i] for i in range(self.num_envs) }
        results     = ac.evaluate_circuit_pool(pool, pool_params = self.sizing)

        state       = filter_results(self.obs_filter, results)
        achieved    = filter_results(self.goal_filter, results)

        observation = OrderedDict({ 'observation':   ( self.obs_scaler(state)
                                                       if self.scale_observation
                                                       else state )
                                  , 'achieved_goal': ( self.goal_scaler(achieved)
                                                       if self.scale_observation
                                                       else achieved )
                                  , 'desired_goal':  ( self.goal_scaler(self.goal)
                                                       if self.scale_observation
                                                       else self.goal ) })

        reward      = self.calculate_reward(observation)

        self.steps  = self.steps + 1

        done        = (reward == 0) | (self.steps >= self.num_steps)

        info        = [{ 'outputs': self.obs_filter
                       , 'goal':    self.goal_filter
                       , 'inputs':  self.input_parameters
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
    def __init__(self, **kwargs):
        """
        Construct Electric Sizing Goal Environment. Same Arguments as
        `CircusGeom`.
        """
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

        self.input_parameters  = electric_identifiers(self.ace_id)

        self.action_space = Box( low   = -1.0
                               , high  = 1.0
                               , shape = (len(self.input_parameters),)
                               , dtype = np.float32 )

        self.unscale_action = electric_unscaler(self.ace_id, self.ace_backend)

    def step_async(self, actions: np.ndarray) -> None:
        unscaled    = list(self.unscale_action(actions))
        self.sizing = { env_id: self.transformation(* action.flatten().tolist())
                        for env_id,action in enumerate(unscaled) }

class CircusGeomVec(CircusGeom):
    """ Geometric Sizing Non-Goal Environment """
    def __init__(self, reward_fn: Callable = dummy_reward, **kwargs):
        """
        Construct Geometric Sizing Non-Goal Environment. Same Arguments as
        `CircusGeom` but different default `reward_fn`.
        """
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
    def __init__(self, reward_fn: Callable = dummy_reward, **kwargs):
        """
        Construct Geometric Sizing Non-Goal Environment. Same Arguments as
        `CircusElec`.
        """
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

def make( env_id: str, n_envs: int = 1, **kwargs
        ) -> Union[CircusGeom, CircusGeomVec]:
    """
    Gym Style Environment Constructor, see `gym.make`.
    Arguments:
        `env_id`: Environment ID of the form '<ace id>-<pdk>-<space>-v<var>
        `n_envs`: Number of Environment
        `kwargs`: Will be passed to Circus constructor.
    """
    eid,pdk,spc,var = env_id.split(':')[1].split('-')
    backend = backend_id(pdk)

    env     = ( CircusGeom( ace_id      = eid
                          , ace_backend = backend
                          , num_envs    = n_envs
                          , **kwargs
                          )    if (var == 'v0' and spc == 'geom') else
                CircusGeomVec( ace_id      = eid
                             , ace_backend = backend
                             , num_envs    = n_envs
                             , **kwargs
                             ) if (var == 'v1' and spc == 'geom') else
                CircusElec( ace_id      = eid
                          , ace_backend = backend
                          , num_envs    = n_envs
                          , **kwargs
                          )    if (var == 'v0' and spc == 'elec') else
                CircusElecVec( ace_id      = eid
                             , ace_backend = backend
                             , num_envs    = n_envs
                             , **kwargs
                             ) if (var == 'v1' and spc == 'elec') else
                NotImplementedError(f'Variant {var} not available') )
    return env
