""" REST API """

from argparse import ArgumentParser
from collections import namedtuple

import numpy as np
import hace as ac
import circus

parser = ArgumentParser()
parser.add_argument( '--host', type = str, default = 'localhost'
                   , help = 'Host address')
parser.add_argument( '-p', '--port', type = int, default = '6007'
                   , help = 'Server Port')
parser.add_argument( '-e', '--env', type = str, default = 'op2'
                   , help = 'ACE Environment ID, see Circus doc for what\'s available')
parser.add_argument( '-s', '--space', type = str, default = 'elec'
                   , help = 'Circus Action Space, see Circus doc for what\'s available')
parser.add_argument( '-v', '--var', type = int, default = '0'
                   , help = 'Circus Environment variant, see Circus doc for what\'s available')
parser.add_argument( '-n', '--num', type = int, default = 1
                   , help = 'Number of Pooled Envs')
parser.add_argument( '-t', '--step', type = int, default = 50
                   , help = 'Number of Steps per Episode')
parser.add_argument( '-c', '--scale', default = True, action = 'store_true'
                   , help = 'Circus Action Space, see Circus doc for what\'s available')
parser.add_argument( '--pdk', type = str, default = 'xh035'
                   , help = 'ACE backend, see Circus doc for what\'s available')

CircusEnv = namedtuple('Environment', 'env ace_id backend space variant num_envs')

def make_env( ace_id: str, backend: str, space: str, variant: int
            , num_envs: int, num_steps: int = 50, scale: bool = True
            ) -> CircusEnv:
    """
    Construct a Circus Environment wrapper for HTTP Access.
    """
    state_filter  = [ 'A', 'a_0', 'cmrr', 'cof', 'gm', 'i_out_max', 'i_out_min'
                    , 'idd', 'iss', 'overshoot_f', 'overshoot_r', 'pm'
                    , 'psrr_n', 'psrr_p', 'sr_f', 'sr_r', 'ugbw', 'v_ih'
                    , 'v_il', 'v_oh', 'v_ol', 'voff_stat', 'voff_sys' ]

    target_filter = ['a_0', 'ugbw', 'pm', 'voff_stat', 'cmrr', 'psrr_p', 'A']

    env_name      = f'circus:{ace_id}-{backend}-{space}-v{variant}'

    env           = circus.make( env_name
                               , n_envs            = num_envs
                               , num_steps         = num_steps
                               , goal_filter       = target_filter
                               , obs_filter        = state_filter
                               , scale_observation = scale
                               , )

    return CircusEnv(env, ace_id, backend, space, variant, num_envs)

def restart(circ: CircusEnv) -> CircusEnv:
    """
    Restart the Environment(s) including ACE.
    """
    env, ace_id, backend, space, variant, num_envs = circ
    return make_env(ace_id, backend, space, variant, num_envs, env.num_steps)

def reset( circ: CircusEnv, env_mask: list[bool] = [], env_ids: list[int] = []
         ) -> dict[str, [[float]]]:
    """
    Reset (selected) Environment(s).
    """
    obs = circ.env.reset(env_mask = env_mask, env_ids = env_ids)
    return { p: o.tolist() for p,o in obs.items() }

def restore( circ: CircusEnv, sizing: dict[str, dict[str, float]]
           ) -> dict[str, [[float]]]:
    """
    Restore a given state.
    """
    circ            = make_env( circ.env_id, circ.pdk, circ.space, circ.var
                              , circ.num, circ.steps, circ.scale )
    circ.env.reset()
    circ.env.sizing = sizing
    observation     = circ.env.step_wait()
    return observation

def restore_last(circ: CircusEnv) -> dict[str, [[float]]]:
    """
    Restore the last state.
    """
    return restore(circ, circ.env.sizing)

def step( circ: CircusEnv, action: dict[str, [[float]]]
        ) -> dict[str, [[float]]]:
    """
    Take a step in the environemt.
    """
    act                = np.array(action['action'])
    obs, rew, don, inf = circ.env.step(act)
    return ( { p:        o.tolist() for p,o in obs.items() }
           | { 'reward': rew.tolist()
             , 'done':   don.tolist()
             , 'info':   inf
             , } )

def random_action(circ: CircusEnv) -> dict[str, [[float]]]:
    """
    Sample a random action action in the environemt.
    """
    action = [ circ.env.action_space.sample().tolist()
               for _ in range(circ.num_envs) ]
    return {'action': action}

def random_step(circ: CircusEnv) -> dict[str, [[float]]]:
    """
    Take a random step in the environemt.
    """
    return step(circ, random_action(circ))

def reward( circ: CircusEnv, observation: dict[str, [[float]]]
          ) -> dict[str, [float]]:
    """
    Calculate reward given an observation Dict.
    """
    obs = { k: np.array(v) for k,v in observation.items() if k != 'info' }
    rew = circ.env.calculate_reward(obs).tolist()
    return {'reward': rew}

def current_performance(circ: CircusEnv) -> dict[int, dict[str, float]]:
    """
    Get current performane from ACE.
    """
    perf = ac.current_performance_pool(circ.env.ace_envs)
    return {i: {o: p[o] for o in circ.env.obs_filter} for i,p in perf.items()}

def current_goal(circ: CircusEnv) -> dict[int, dict[str, float]]:
    """
    Get goals for the current episode.
    """
    return dict(enumerate(list(map( lambda g: dict(zip(circ.env.goal_filter, g))
                                  , circ.env.goal.tolist() ))))

def current_sizing(circ: CircusEnv) -> dict[int, dict[str, float]]:
    """
    Get the current sizing from ACE.
    """
    return ac.current_sizing_pool(circ.env.ace_envs)

def last_action(circ: CircusEnv) -> dict[int, dict[str, float]]:
    """
    Get the last action that was taken. Will be same as sizing if 
    `space == 'geom'` otherwise it will be INPUTS.
    """
    return { i: { k: v for k,v in p.items() if k in circ.env.input_parameters }
             for i,p in ac.current_performance_pool(circ.env.ace_envs).items() }

def action_space(circ: CircusEnv) -> dict[int, int]:
    """
    Shape of action space.
    """
    return { 'action': circ.env.action_space.shape[0] }

def observation_space(circ: CircusEnv) -> dict[int, int]:
    """
    Shape of observation space.
    """
    return { o: s.shape[0] for o,s in circ.env.observation_space.items() }

def action_keys(circ: CircusEnv) -> dict[int, [str]]:
    """
    Keys in action vector.
    """
    return { 'action': circ.env.input_parameters }

def observation_keys(circ: CircusEnv) -> dict[int, [str]]:
    """
    Keys in observation vector.
    """
    return { 'observation': circ.env.obs_filter }

def goal_keys(circ: CircusEnv) -> dict[int, [str]]:
    """
    Keys in goal vector.
    """
    return { 'goal': circ.env.goal_filter }
