""" Gym compatible Analog Circuit Environment """

import os
import errno
from   functools   import partial
from   collections import OrderedDict
from   typing      import Any, List, Optional, Type, Union, Callable, Mapping, Iterable
import gym
from   gym.spaces import Dict, Box
from   gym        import GoalEnv
from   stable_baselines3.common.vec_env.base_vec_env import VecEnv, \
                                                            VecEnvIndices, \
                                                            VecEnvStepReturn
import json
import numpy     as np
import torch     as pt
import pyspectre as ps
import serafin   as sf

from .util    import *
from .reward  import *
from .trafo   import *
from .seraf   import *

class CircusGeom(GoalEnv, VecEnv):
    """ Geometric Sizing Goal Environment """
    def __init__( self
                , ckt_id: str
                , pdk_id: str
                , ckt_cfg: str                     = None
                , pdk_cfg: str                     = None
                , netlist: str                     = None
                , num_envs: int                    = 1
                , num_steps: int                   = 50
                , seed: int                        = 666
                , obs_filter: Union[str,List[str]] = 'perf'
                , goal_filter: list[str]           = None
                , goal_preds: list[Callable]       = None
                , goal_init: Union[str,np.ndarray] = 'noisy'
                , reward_fn: Callable              = None
                , scale_observation: bool          = True
                , auto_reset: bool                 = False
                , ):
        """
        Construct a Geometric Sizing Goal Environment
        Arguments:
            - `ckt_id`:            3 Letter ID, see serafin Documentation for
                                   further details.
            - `pdk_id`:            PDK, available are 'xt018', 'xh018',
                                   'gpdk180', 'gpdk090', 'gpdk045'
            - `ckt_cfg`:           Path to `ckt_id.yml`, if not providied it
                                   will be searched for in default locations
            - `pdk_cfg`:           Path to `pdk_id.yml`, if not provided it
                                   will be searched for in default locations
            - `netlist`:           Path to OpAmp netlist. if not provieded it
                                   will be searched for in default locations
            - `num_envs`:          Numer of Parallel Environments ∈ [ 1 .. ∞]
            - `num_steps`:         Number of steps per Episode.
            - `seed`:              Random Seed
            - `obs_filter`:        Filter Performance dict obtained from serafin:
                                   'perf': Only performance paramters (default),
                                   'all': All parameters from serafin,
                                   [str]: List of parameters
            - `goal_filter`:       Optional list of parameters
            - `goal_preds`:        Binary comparison operators
            - `goal_init`:         How to initialize new goals on reset:
                                   'noisy': Put some noise on a reference goal (default),
                                   'random': Choose a point in goal space,
                                   np.ndarray: A specific fix goal of shape
                                   (num_envs, len(goal_filter)).
            - `reward_fn`:         Optional reward function that takes an observation dict.
            - `scale_observation`: Scale the observations and goals as
                                   specified in trafo (default = True)
            - `auto_reset`:        Automatically reset environemt when done (default = False).
        """

        self.ckt_id: str       = ckt_id
        self.pdk_id: str       = pdk_id
        self.num_envs: int     = num_envs

        self.circus_home       = os.environ.get( 'CIRCUS_HOME'
                                               , os.path.expanduser('~/.circus'))
        self.ckt_cfg           = ckt_cfg if ckt_cfg and os.path.isfile(ckt_cfg) \
                                    else f'{self.circus_home}/ckt/{self.ckt_id}.yml'
        self.pdk_cfg           = pdk_cfg if pdk_cfg and os.path.isfile(pdk_cfg) \
                                    else f'{self.circus_home}/pdk/{self.pdk_id}.yml'
        self.netlist           = netlist if netlist and os.path.isfile(netlist) \
                                    else f'{self.circus_home}/pdk/{self.pdk_id}/{self.ckt_id}.scs'

        self.op_amps           = make_ops( self.ckt_cfg, self.pdk_cfg
                                         , self.netlist, self.num_envs )

        self.auto_reset: bool  = auto_reset

        self.num_steps: int    = num_steps
        self.steps: np.array   = np.zeros(num_envs)


        self.constraints       = self.op_amps[0].parameters \
                               | self.op_amps[0].constraints

        _                      = set_parameters( self.op_amps
                                               , [ p.parameters
                                                   for p in self.op_amps ] )

        pf_ids                 = sorted(list(self.op_amps[0].performances.keys()))
        op_ids                 = sorted(list(self.op_amps[0].dcop_params.keys()))
        of_ids                 = sorted(list(self.op_amps[0].offs_params.keys()))

        if obs_filter == 'all':
            self.obs_filter    = sorted(pf_ids + op_ids + of_ids)
        elif obs_filter == 'perf':
            self.obs_filter    = sorted(pf_ids)
        elif isinstance(obs_filter, Iterable) and \
                (set(obs_filter) <= set(pf_ids + op_ids + of_ids)):
            self.obs_filter    = sorted(obs_filter)
        else:
            raise(ValueError( errno.EINVAL, os.strerror(errno.EINVAL)
                            , f'Invalid Argument obs_filter: {obs_filter}'))

        self.obs_scaler,\
        self.obs_unscaler      = performance_scaler( self.ckt_id
                                                   , self.constraints
                                                   , self.obs_filter
                                                   , )

        self.input_parameters  = sorted(list(self.op_amps[0].geom_init.keys()))

        self.goal_filter       = sorted(goal_filter or [ ident for ident
                                                         in self.obs_filter
                                                         if ident.islower() ])

        self.goal_idx          = np.array([ i for i,p in enumerate(self.obs_filter)
                                              if p in self.goal_filter ])

        self.goal_preds        = goal_preds or goal_predicate(self.goal_filter)

        self.goal_scaler, \
        self.goal_unscaler     = performance_scaler( self.ckt_id
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

        self.sizing            = pd.DataFrame.from_dict({ k: [v] for k,v in
                                                          self.op_amps[0].geom_init.items()})
        self.last_obs          = evaluate(self.op_amps, self.sizing)

        if isinstance(goal_init, str) and goal_init == 'noisy':
            self.goal_init      = goal_init
            ref_goal_op         = reference_goal(self.ckt_id, self.constraints)
            ref_goal            = self.last_obs[[c for c in self.goal_filter
                                                   if c in self.last_obs.columns]
                                               ].join(ref_goal_op[[c for c in self.goal_filter
                                                                     if c not in self.last_obs.columns]])
            ref_goals           = ref_goal.iloc[ np.arange(len(ref_goal)
                                                          ).repeat(self.num_envs)
                                               ].reset_index()
            self.reference_goal = filter_results( self.goal_filter
                                                , ref_goals )
        # elif isinstance(goal_init, str) and goal_init == 'random':
        #     self.goal_init      = goal_init
        #     x_min_d, x_max_d    = performance_scale( self.ace_id
        #                                            , self.ace_backend
        #                                            , self.constraints
        #                                            , )
        #     self.reference_goal = np.array([ [x_min_d[gp] for gp in self.goal_filter]
        #                                    , [x_max_d[gp] for gp in self.goal_filter]
        #                                    ])
        # elif isinstance(goal_init, np.ndarray):
        #     self.goal_init      = 'fix'
        #     goal_shape          = (num_envs, len(self.goal_filter))
        #     self.reference_goal = ( goal_init
        #                             if goal_init.shape == goal_shape else
        #                             np.repeat(goal_init[None], num_envs, axis = 0) )
        else:
            NotImplementedError(f'Goal initializer {goal_init} not available.')

        self.new_goal          = goal_generator( self.goal_init
                                               , self.reference_goal
                                               , )
        self.goal              = self.new_goal()

        self.act_unscaler      = geometric_unscaler( self.constraints
                                                   , self.input_parameters )

        VecEnv.__init__( self, self.num_envs
                       , self.observation_space
                       , self.action_space )

    def close(self, env_ids: Iterable[int] = None) -> None:
        """
        Close all (parallel) serafin session(s).
        Arguments:
            - `env_ids`: List of environment IDs that will be closed.
                         Default = None closes all.
        """
        for i in (env_ids or range(self.num_envs)):
            ps.stop_session(self.op_amps[i].session, True)

    def observation_dict( self, observation: pd.DataFrame
                        ) -> dict[str, np.ndarray]:
        """
        Takes an observation from a serafin evaluation and returns a
        `GoalEnv` compliant `OrderedDict`.
        """
        state       = filter_results(self.obs_filter, observation).values
        achieved    = filter_results(self.goal_filter, observation).values
        desired     = self.goal.values

        obs         = np.nan_to_num( self.obs_scaler(state)
                                     if self.scale_observation else state )
        a_goal      = np.nan_to_num( self.goal_scaler(achieved)
                                     if self.scale_observation else achieved )
        d_goal      = np.nan_to_num( self.goal_scaler(desired)
                                     if self.scale_observation else self.goal )

        return OrderedDict({ 'observation':   obs
                           , 'achieved_goal': a_goal
                           , 'desired_goal':  d_goal })

    def reset(self, env_mask: list[bool] = [], env_ids: list[int] = []):
        """
        Reset all (parallel) environment(s).
        Arguments:
            - `env_mask`: Boolean mask of environemts that will be reset.
                          Passing the `done` vector works. This argument is
                          prioritized over `env_ids`.
            - `env_ids`: List of integer IDs of environments that will be reset.
                         This argument is discarded in favour of `env_mask` if
                         given.
        """

        reset_ids             = [ i for i,m in enumerate(env_mask) if m
                                ] or env_ids or range(self.num_envs)
        const_ids             = [ i for i in range(self.num_envs)
                                    if i not in reset_ids ]

        cur_sizing            = current_sizing(self.op_amps)
        rng_sizing            = random_sizing(self.op_amps)
        self.sizing           = pd.concat( [ cur_sizing.iloc[const_ids]
                                           , rng_sizing.iloc[reset_ids] ]
                                         , axis = 0
                                         ).sort_index()

        self.last_obs         = evaluate(self.op_amps, self.sizing)

        self.goal             = pd.concat( [ self.goal.iloc[const_ids]
                                           , self.new_goal().iloc[reset_ids]]
                                         , axis = 0
                                         ).sort_index()

        observation           = self.observation_dict(self.last_obs)

        self.steps[reset_ids] = 0

        return observation

    def step(self, actions: np.ndarray) -> VecEnvStepReturn:
        """
        Take a step in the Environment. Calls `step_async` and `step_wait`
        under the hood.
        Arguments:
            - `actions`: Take Action with shape [num_envs, action_space].
        """
        self.step_async(actions)
        return self.step_wait()

    def step_async(self, actions: np.ndarray) -> None:
        """
        Initiate a step in the Environment by storing the action to
        `self.sizing`.
        Arguments:
            - `actions`: Take Action with shape [num_envs, action_space].
        """

        unscaled    = self.act_unscaler(np.clip( actions
                                               , self.action_space.low
                                               , self.action_space.high ))
        self.sizing = pd.DataFrame(unscaled, columns = self.input_parameters)

    def step_wait(self) -> VecEnvStepReturn:
        """
        Complete a step in the Environment by evaluating `self.sizing`.
        """
        self.last_obs = evaluate(self.op_amps, self.sizing)
        observation   = self.observation_dict(self.last_obs)
        reward        = self.calculate_reward(observation)
        self.steps    = self.steps + 1
        done          = (reward == 0) | (self.steps >= self.num_steps)
        info_dict     = { 'outputs': self.obs_filter
                        , 'goal':    self.goal_filter
                        , 'inputs':  self.input_parameters
                        , }
        info          = [ info_dict | {'is_success': s}
                          for s in (reward == 0).tolist() ]

        if self.auto_reset and done.any():
            for idx,inf in enumerate(info):
                inf["terminal_obs"] = observation["observation"][idx]
                inf["target"]       = observation["desired_goal"][idx]
            observation = self.reset(done)



        return (observation, reward, done, info)

    def compute_reward( self, achieved_goal: object, desired_goal: object
                      , info: Mapping[str, Any] ) -> np.array:
        """
        Externalized reward calculation for stable baselines compatibility.
        Calls `self.calculate_reward` under the hood.
        """
        observation = { "achieved_goal": achieved_goal
                      , "desired_goal":  desired_goal
                      , }
        return self.calculate_reward(observation = observation)

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
        """
        Construct Electric Sizing Goal Environment. Same Arguments as
        `CircusGeom`.
        """
        super().__init__(**kwargs)

        nmos_path = os.path.expanduser(f'~/.circus/pdk/{self.pdk_id}/nmos.pt')
        pmos_path = os.path.expanduser(f'~/.circus/pdk/{self.pdk_id}/pmos.pt')

        self.nmos = pt.jit.load(nmos_path).cpu().eval()
        self.pmos = pt.jit.load(pmos_path).cpu().eval()

        self.transformation = partial( transformation(self.ckt_id)
                                     , self.constraints
                                     , self.nmos
                                     , self.pmos
                                     , )

        self.input_parameters  = electric_identifiers(self.ckt_id)

        self.action_space      = Box( low   = -1.0
                                    , high  = 1.0
                                    , shape = (len(self.input_parameters),)
                                    , dtype = np.float32 )

        self.act_unscaler      = electric_unscaler(self.ckt_id)

    def step_async(self, actions: np.ndarray) -> None:
        """
        Initiate a step in the Environment by transforming the action in the
        elctrical space to geometric sizing parameters and storing it to
        `self.sizing`.
        Arguments:
            - `actions`: Take Action with shape [num_envs, action_space].
        """
        unscaled    = self.act_unscaler(np.clip( actions
                                               , self.action_space.low
                                               , self.action_space.high ))

        self.sizing = pd.concat([ self.transformation(*action.tolist())
                                  for action in list(unscaled) ])

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
        """
        Same as Parent `reset` in `CircusGeom` but returns only the
        'obervation' field.
        """
        obs = super().reset(**kwargs)
        return obs['observation']

    def step_wait(self) -> VecEnvStepReturn:
        """
        Same as Parent `step_wait` in `CircusGeom` but returns only the
        'obervation' field of the observation, no goal.
        """
        obs, reward, done, info = super().step_wait()
        observation        = obs['observation']
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
        """
        Same as Parent `reset` in `CircusElec` but returns only the
        'obervation' field.
        """
        obs = super().reset(**kwargs)
        return obs['observation']

    def step_wait(self) -> VecEnvStepReturn:
        """
        Same as Parent `step_wait` in `CircusElec` but returns only the
        'obervation' field of the observation, no goal.
        """
        obs, reward, done, info = super().step_wait()
        observation        = obs['observation']
        return (observation, reward, done, info)

def make( env_id: str, n_envs: int = 1, **kwargs
        ) -> Union[CircusGeom, CircusGeomVec]:
    """
    Gym Style Environment Constructor, see `gym.make`.
    Arguments:
        - `env_id`: Environment ID of the form '<ckt id>-<pdk id>-<space>-v<var>
        - `n_envs`: Number of Environment
        - `kwargs`: Will be passed to Circus constructor.
    """
    eid,pdk,spc,var = env_id.split(':')[1].split('-')

    env     = ( CircusGeom( ckt_id   = eid
                          , pdk_id   = pdk
                          , num_envs = n_envs
                          , **kwargs
                          ) if (var == 'v0' and spc == 'geom') else
                CircusGeomVec( ckt_id   = eid
                             , pdk_id   = pdk
                             , num_envs = n_envs
                             , **kwargs
                             ) if (var == 'v1' and spc == 'geom') else
                CircusElec( ckt_id   = eid
                          , pdk_id   = pdk
                          , num_envs = n_envs
                          , **kwargs
                          )    if (var == 'v0' and spc == 'elec') else
                CircusElecVec( ckt_id   = eid
                             , pdk_id   = pdk
                             , num_envs = n_envs
                             , **kwargs
                             ) if (var == 'v1' and spc == 'elec') else
                NotImplementedError(f'Variant {var} not available') )
    return env
