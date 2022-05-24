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

def make_vec_env(env_id: str, n_envs: int, **kwargs):
    envs = [gym.make(env_id, **kwargs) for _ in range(n_envs)]
    return VecEnvWrapper(envs)

def make_goal_env(env_id: str, n_envs: int, **kwargs):
    envs = [gym.make(env_id, **kwargs) for _ in range(n_envs)]
    return GoalEnvWrapper(envs)

class Circus(Env):
    """Goal based circuit sizing environment."""
    def __init__( self
                , ace_id: str
                , ace_backend: str
                , num_steps: int   = 50
                , seed: int        = 666
                , ):
        self.ace_id: str       = ace_id
        self.ace_backend: str  = ace_backend
        self.num_steps: int    = num_steps
        self.steps: int        = 0
        self.ace_env           = ac.make_env(self.ace_id, self.ace_backend)

        param_dict             = ac.parameter_dict(self.ace_env)
        self.action_min        = np.array([ v["min"] for _,v
                                            in sorted( param_dict.items()
                                                     , key = lambda kv: kv[0] )
                                            if v["sizing"] ])
        self.action_max        = np.array([ v["max"] for _,v
                                            in sorted( param_dict.items()
                                                     , key = lambda kv: kv[0] )
                                            if v["sizing"] ])

        num_acts               = len(ac.sizing_identifiers(self.ace_env))
        num_obs                = len(ac.performance_identifiers(self.ace_env))

        self.action_space      = Box( low   = -1.0
                                    , high  = 1.0
                                    , shape = (num_acts,)
                                    , dtype = np.float32 )

        self.observation_space = Box(low = -np.Inf, high = np.Inf
                                    , shape = (num_obs,)
                                    , dtype = np.float32 )

        self.seed              = seed

    def calculate_reward(self, observation):
        dim = len(observation.shape) - 1
        return np.sum(observation, axis = dim)

    def reset(self) -> np.array:
        self.ace_env.clear()
        self.ace_env = ac.make_env(self.ace_id, self.ace_backend)
        sizing       = ac.random_sizing(self.ace_env)
        results      = ac.evaluate_circuit(self.ace_env, params = sizing)
        observation  = np.array([p for _,p in sorted( results.items()
                                                    , key = lambda kv: kv[0])])
        self.steps   = 0
        return observation

    def step(self, action: np.array) -> tuple[np.array, float, bool, dict]:

        unscaled    = self.action_min + ((action + 1.0) / 2.0) * (self.action_max - self.action_min)
        sizing      = dict(zip( sorted(ac.sizing_identifiers(self.ace_env))
                              , unscaled.tolist()))
        results     = ac.evaluate_circuit(self.ace_env, params = sizing)
        observation = np.array([p for _,p in sorted( results.items()
                                                   , key = lambda kv: kv[0])])
        reward      = self.calculate_reward(observation)
        done        = self.steps >= self.num_steps
        info        = { 'outputs': sorted(list(results.keys()))
                      , 'inputs':  sorted(ac.sizing_identifiers(self.ace_env)) }
        self.steps  = self.steps + 1
        return (observation, reward, done, info)

    def close(self):
        self.ace_env.clear()
        del self.ace_env

    def render(self, mode: str = "human"):
        pass

class GoalEnvWrapper(GoalEnv, VecEnv):
    def __init__(self, envs, goal_ids: [str] = [], goal_preds: [Callable] = []):

        performance_ids = sorted(ac.performance_identifiers(envs[0].ace_env))

        self.goal_ids   = goal_ids or [ident for ident in performance_ids
                                             if ident.islower() or (ident == "A")]

        self.goal_idx   = np.array([i for i,p in enumerate(performance_ids)
                                      if p in self.goal_ids])

        self.goal_preds = [ operator.le # Area (A)
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

        self.envs     = envs
        self.num_envs = len(envs)

        self.action_space      = envs[0].action_space
        self.observation_space = Dict({ 'observation':   envs[0].observation_space
                                      , 'achieved_goal': Box( -np.Inf, np.Inf
                                                            , (len(self.goal_ids),))
                                      , 'desired_goal':  Box( -np.Inf, np.Inf
                                                            , (len(self.goal_ids),))
                                      })

        pool                = { i: self.envs[i].ace_env for i in range(self.num_envs) }
        initial_sizing      = ac.initial_sizing_pool(pool)
        results             = ac.evaluate_circuit_pool(pool, pool_params = initial_sizing)
        self.reference_goal = np.array([ [ p for k,p in r.items() if k in self.goal_ids]
                                             for r in results.values() ])
        self.goal           = self.reference_goal

        self.action_min       = envs[0].action_min
        self.action_max       = envs[0].action_max
        self.sizing           = {}
        self.num_steps        = envs[0].num_steps
        self.steps            = 0

        VecEnv.__init__(self, len(envs), self.observation_space, self.action_space)

    def close(self) -> None:
        for env in self.envs:
            env.close()

    def add_noise(self, x: np.array, noise: float = 0.1):
        dim = x.shape
        return (x + (x * np.random.normal(np.ones(dim), np.full(dim, noise))))

    def reset(self, env_mask: [bool] = [], env_ids: [int] = []):
        reset_ids     = [i for i,m in enumerate(env_mask) if m] or env_ids or range(self.num_envs)
        pool          = { i: self.envs[i].ace_env for i in reset_ids}
        random_sizing = ac.random_sizing_pool(pool)
        results       = ac.evaluate_circuit_pool(pool, pool_params = random_sizing)
        state         = np.vstack([ np.array([p for _,p in sorted( results[i].items()
                                                                 , key = lambda kv: kv[0])])
                                    for i in range(len(results)) ])
        self.goal     = self.add_noise(self.reference_goal)
        achieved      = ( state[:,self.goal_idx] if (len(state.shape) > 1)
                                               else state[self.goal_idx] )
        observation   = OrderedDict({ 'observation': state
                                    , 'achieved_goal': achieved
                                    , 'desired_goal': self.goal })
        return observation

    def step(self, action: [np.array]) -> VecEnvStepReturn:
        self.step_async(np.vstack(action))
        return self.step_wait()

    def step_async(self, actions: np.ndarray) -> None:
        unscaled = self.action_min + ( ((np.vstack(actions) + 1.0) / 2.0)
                                     * (self.action_max - self.action_min))

        params = sorted(ac.sizing_identifiers(self.envs[0].ace_env))

        sizing = { k: dict(zip(params, v.tolist()))
                   for k,v in enumerate(list(unscaled))}

        self.sizing = sizing

    def step_wait(self) -> VecEnvStepReturn:
        pool        = { i: self.envs[i].ace_env
                        for i in range(self.num_envs) }
        results     = ac.evaluate_circuit_pool(pool, pool_params = self.sizing)

        obs = np.vstack([ np.array([p for _,p in sorted( results[i].items()
                                       , key = lambda kv: kv[0])])
                                  for i in range(len(results)) ])
        achieved             = ( obs[:,self.goal_idx] if (len(obs.shape) > 1)
                                                    else obs[self.goal_idx] )
        observation          = OrderedDict({ 'observation': obs
                                           , 'achieved_goal': achieved
                                           , 'desired_goal': self.goal })

        reward      = np.array([ (p(g,a) - 1.0) for p,g,a in zip( self.goal_preds
                                                                , self.goal.tolist()
                                                                , achieved.tolist()) ])

        done        = np.array([env.steps >= env.num_steps for env in self.envs])
        info        = [{ 'outputs': sorted(list(results[0].keys()))
                       , 'inputs':  sorted(ac.sizing_identifiers(self.envs[0].ace_env)) }]

        for env in self.envs:
            env.steps = env.steps + 1

        return (observation, reward, done, info)

    def get_attr( self, attr_name: str, indices: VecEnvIndices = None
                ) -> List[Any]:
        """Return attribute from vectorized environment (see base class)."""
        target_envs = self._get_target_envs(indices)
        return [getattr(env_i, attr_name) for env_i in target_envs]

    def set_attr( self, attr_name: str, value: Any
                , indices: VecEnvIndices = None) -> None:
        """Set attribute inside vectorized environments (see base class)."""
        target_envs = self._get_target_envs(indices)
        for env_i in target_envs:
            setattr(env_i, attr_name, value)

    def env_method( self, method_name: str, *method_args
                  , indices: VecEnvIndices = None, **method_kwargs
                  ) -> List[Any]:
        """Call instance methods of vectorized environments."""
        target_envs = self._get_target_envs(indices)
        return [ getattr(env_i, method_name)(*method_args, **method_kwargs)
                 for env_i in target_envs ]

    def env_is_wrapped( self, wrapper_class: Type[gym.Wrapper]
                      , indices: VecEnvIndices = None) -> List[bool]:
        """Check if worker environments are wrapped with a given wrapper"""
        return [False for _ in range(self.num_envs)]

    def _get_target_envs(self, indices: VecEnvIndices) -> List[gym.Env]:
        return [self.envs]

    def seed(self, seed: Optional[int] = None) -> List[Union[None, int]]:
        return [env.seed for env in self.envs]

    def render(self, mode: str = "human") -> Optional[np.ndarray]:
        pass


class VecEnvWrapper(VecEnv):
    def __init__(self, envs):
        self.envs             = envs
        self.num_envs         = len(envs)
        observation_space     = envs[0].observation_space
        action_space          = envs[0].action_space
        self.action_min       = envs[0].action_min
        self.action_max       = envs[0].action_max
        self.sizing           = {}
        self.num_steps        = envs[0].num_steps
        self.calculate_reward = envs[0].calculate_reward
        self.steps            = 0

        super().__init__(len(envs), observation_space, action_space)

    def close(self) -> None:
        for env in self.envs:
            env.close()

    def step(self, action: [np.array]) -> VecEnvStepReturn:
        self.step_async(np.vstack(action))
        return self.step_wait()

    def step_async(self, actions: np.ndarray) -> None:
        unscaled = self.action_min + ( ((np.vstack(actions) + 1.0) / 2.0)
                                     * (self.action_max - self.action_min))

        params = sorted(ac.sizing_identifiers(self.envs[0].ace_env))

        sizing = { k: dict(zip(params, v.tolist()))
                   for k,v in enumerate(list(unscaled))}

        self.sizing = sizing

    def step_wait(self) -> VecEnvStepReturn:
        pool        = { i: self.envs[i].ace_env
                        for i in range(self.num_envs) }
        results     = ac.evaluate_circuit_pool(pool, pool_params = self.sizing)
        observation = np.vstack([ np.array([p for _,p in sorted( results[i].items()
                                       , key = lambda kv: kv[0])])
                                  for i in range(len(results)) ])
        reward      = self.calculate_reward(observation)
        done        = np.array([env.steps >= env.num_steps for env in self.envs])
        info        = [{ 'outputs': sorted(list(results[0].keys()))
                       , 'inputs':  sorted(ac.sizing_identifiers(self.envs[0].ace_env)) }]
        for env in self.envs:
            env.steps = env.steps + 1
        return (observation, reward, done, info)

    def reset(self, env_mask: [bool] = [], env_ids: [int] = []):
        reset_ids     = [i for i,m in enumerate(env_mask) if m] or env_ids or range(self.num_envs)
        pool          = { i: self.envs[i].ace_env for i in reset_ids}
        random_sizing = ac.random_sizing_pool(pool)
        results       = ac.evaluate_circuit_pool(pool, pool_params = random_sizing)
        observation   = np.vstack([ np.array([p for _,p in sorted( results[i].items()
                                                                 , key = lambda kv: kv[0])])
                                    for i in range(len(results)) ])
        return observation

    def get_attr( self, attr_name: str, indices: VecEnvIndices = None
                ) -> List[Any]:
        """Return attribute from vectorized environment (see base class)."""
        target_envs = self._get_target_envs(indices)
        return [getattr(env_i, attr_name) for env_i in target_envs]

    def set_attr( self, attr_name: str, value: Any
                , indices: VecEnvIndices = None) -> None:
        """Set attribute inside vectorized environments (see base class)."""
        target_envs = self._get_target_envs(indices)
        for env_i in target_envs:
            setattr(env_i, attr_name, value)

    def env_method( self, method_name: str, *method_args
                  , indices: VecEnvIndices = None, **method_kwargs
                  ) -> List[Any]:
        """Call instance methods of vectorized environments."""
        target_envs = self._get_target_envs(indices)
        return [ getattr(env_i, method_name)(*method_args, **method_kwargs)
                 for env_i in target_envs ]

    def env_is_wrapped( self, wrapper_class: Type[gym.Wrapper]
                      , indices: VecEnvIndices = None) -> List[bool]:
        """Check if worker environments are wrapped with a given wrapper"""
        return [False for _ in range(self.num_envs)]

    def _get_target_envs(self, indices: VecEnvIndices) -> List[gym.Env]:
        return [self.envs]

    def seed(self, seed: Optional[int] = None) -> List[Union[None, int]]:
        return [env.seed for env in self.envs]

    def render(self, mode: str = "human") -> Optional[np.ndarray]:
        pass
