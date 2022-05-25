"""Circus"""

import operator
from collections import OrderedDict
from typing import Any, List, Optional, Type, Union, Callable
import gym
from gym.spaces import Dict, Box
from gym import Env, GoalEnv
from stable_baselines3.common.vec_env.base_vec_env import VecEnv, \
                                                          VecEnvIndices, \
                                                          VecEnvStepReturn

import numpy as np
import hace as ac

def backend_id(pdk:str) -> str:
    return (pdk + '-3V3' if pdk == 'xh035'  else
            pdk + '-1V8' if pdk == 'xh018'  else
            pdk + '-1V8' if pdk == 'xt018'  else
            pdk + '-1V8' if pdk == 'sky130' else
            pdk)

def default_reward(observation) -> np.array:
    return np.sum(observation, axis = 1)

def add_noise(x: np.array, noise: float = 0.1) -> np.array:
    dim = x.shape
    return (x + (x * np.random.normal(np.ones(dim), np.full(dim, noise))))

class CircusGeom(GoalEnv, VecEnv):
    def __init__( self
                , ace_id: str
                , ace_backend: str
                , num_envs: int          = 1
                , num_steps: int         = 50
                , seed: int              = 666
                , goal_ids: [str]        = []
                , goal_preds: [Callable] = []
                , reward_fn: Callable    = default_reward
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

        self.goal_preds        = [ operator.le # Area (A)
                                 , operator.ge # Gain (A_0)
                                 , operator.ge # Common Mode Rejection Ration (CMRR)
                                 , operator.ge # Cross over Frequency (COF)
                                 , operator.le # Gain Margin (GM)
                                 , operator.ge # Maximum Output Current
                                 , operator.ge # Minimum Output Current
                                 , operator.ge # Current Consumption
                                 , operator.ge # Current Consumption
                                 , operator.ge # Slew Rate Overswing Falling
                                 , operator.ge # Slew Rate Overswing Rising
                                 , operator.ge # Phase Margin (PM)
                                 , operator.ge # Power Supply Rejection Ratio - (PSRR_n)
                                 , operator.ge # Power Supply Rejection Ratio + (PSRR_p)
                                 , operator.le # Slew Rate Falling
                                 , operator.ge # Slew Rate Rising
                                 , operator.ge # Unity Gain Bandwidth Product (UGBW)
                                 , operator.ge # Input High
                                 , operator.ge # Input Low
                                 , operator.ge # Ouput High
                                 , operator.ge # Ouput Low
                                 , operator.ge # Statistical Offset
                                 , operator.le # Systematic Offset
                                 ]

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

        param_dict             = ac.parameter_dict(self.ace_envs[0])
        self.action_min        = np.array([ v['min'] for _,v
                                            in sorted( param_dict.items()
                                                     , key = lambda kv: kv[0] )
                                            if v['sizing'] ])
        self.action_max        = np.array([ v['max'] for _,v
                                            in sorted( param_dict.items()
                                                     , key = lambda kv: kv[0] )
                                            if v['sizing'] ])

        self.sizing            = {}

        VecEnv.__init__( self, self.num_envs
                       , self.observation_space
                       , self.action_space )

    def close(self) -> None:
        for env in self.ace_envs:
            env.close()

    def reset(self, env_mask: [bool] = [], env_ids: [int] = []):
        reset_ids     = [ i for i,m in enumerate(env_mask) if m
                        ] or env_ids or range(self.num_envs)
        pool          = { i: self.ace_envs[i] for i in reset_ids }
        random_sizing = ac.random_sizing_pool(pool)
        results       = ac.evaluate_circuit_pool(pool, pool_params = random_sizing)
        state         = np.vstack([ np.array([p for _,p in sorted( results[i].items()
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

    def step(self, action: [np.array]) -> VecEnvStepReturn:
        self.step_async(np.vstack(action))
        return self.step_wait()

    def step_async(self, actions: np.ndarray) -> None:
        unscaled = self.action_min + ( ((np.vstack(actions) + 1.0) / 2.0)
                                     * (self.action_max - self.action_min))

        params = sorted(ac.sizing_identifiers(self.ace_envs[0]))

        sizing = { k: dict(zip(params, v.tolist()))
                   for k,v in enumerate(list(unscaled))}

        self.sizing = sizing

    def step_wait(self) -> VecEnvStepReturn:
        pool        = { i: self.ace_envs[i]
                        for i in range(self.num_envs) }
        results     = ac.evaluate_circuit_pool(pool, pool_params = self.sizing)

        obs         = np.vstack([ np.array([p for _,p in sorted( results[i].items()
                                                               , key = lambda kv: kv[0])])
                                  for i in range(len(results)) ])
        achieved    = ( obs[:,self.goal_idx] if (len(obs.shape) > 1)
                                             else obs[self.goal_idx] )
        observation = OrderedDict({ 'observation': obs
                                  , 'achieved_goal': achieved
                                  , 'desired_goal': self.goal })

        reward      = np.array([ (p(g,a) - 1.0) for p,g,a in zip( self.goal_preds
                                                                , self.goal.tolist()
                                                                , achieved.tolist()) ])

        self.steps  = self.steps + 1

        done        = self.steps >= self.num_steps

        info        = [{ 'outputs': sorted(list(results[0].keys()))
                       , 'inputs':  sorted(ac.sizing_identifiers(self.ace_envs[0])) }
                      ] * self.num_envs

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

class CircusGeomVec(CircusGeom):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
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
                                                         , CircusGeomVec
                                                         ]:
    id,pdk,space,var = env_id.split(':')[1].split('-')
    backend = backend_id(pdk)
    env     = ( CircusGeom( ace_id = id
                          , ace_backend = backend
                          , num_envs = n_envs
                          , **kwargs 
                          )    if var == "v0" else
                CircusGeomVec( ace_id = id
                             , ace_backend = backend
                             , num_envs = n_envs
                             , **kwargs 
                             ) if var == "v1" else
                NotImplementedError(f'Variant {var} not available') )
    return env
