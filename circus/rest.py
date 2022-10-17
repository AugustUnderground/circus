""" REST API """

from   typing      import Union
from   argparse    import ArgumentParser
from   collections import namedtuple

import numpy         as np
import circus.circus as ckt
# import circus.seraf  as sfu
from   .util       import df_to_dict

parser = ArgumentParser()
parser.add_argument( '--host', type = str, default = 'localhost'
                   , help = 'Host address')
parser.add_argument( '-p', '--port', type = int, default = '6007'
                   , help = 'Server Port')
parser.add_argument( '-e', '--env', type = str, default = 'op2'
                   , help = 'Serafin circuit ID, see Circus doc for what\'s available')
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
                   , help = 'PDK ID, see Circus doc for what\'s available')
parser.add_argument( '-gn', '--goals', nargs = '+', default = []
                   , help = 'List of goal parameters.')
parser.add_argument( '-o', '--states', nargs = '+', default = []
                   , help = 'List of observation / state parameters.')

CircusEnv = namedtuple('Environment', 'env ckt_id pdk_id space variant num_envs')

def make_env( ckt_id: str, pdk_id: str, space: str, variant: int
            , n_envs: int, n_steps: int = 50, scale: bool = True
            , obs_filter: Union[str, list[str]] = 'perf'
            , goal_filter: Union[str, list[str]] = 'perf'
            ) -> CircusEnv:
    """
    Construct a Circus Environment wrapper for HTTP Access.
    """

    env_name      = f'circus:{ckt_id}-{pdk_id}-{space}-v{variant}'

    env           = ckt.make( env_name
                            , n_envs            = n_envs
                            , num_steps         = n_steps
                            , goal_filter       = goal_filter
                            , obs_filter        = obs_filter
                            , scale_observation = scale
                            , )

    return CircusEnv(env, ckt_id, pdk_id, space, variant, n_envs)

def restart(circ: CircusEnv) -> CircusEnv:
    """
    Restart the Environment(s)
    """
    env, ckt_id, pdk_id, space, variant, num_envs = circ
    return make_env(ckt_id, pdk_id, space, variant, num_envs, env.num_steps)

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
    obs = { k: np.array(v)
            for k,v in observation.items()
            if k in ['observation', 'desired_goal', 'achieved_goal'] }

    rew = circ.env.calculate_reward(obs).tolist()
    return {'reward': rew}

def current_performance(circ: CircusEnv) -> dict[int, dict[str, float]]:
    """
    Get current performane from ACE.
    """
    return df_to_dict(circ.env.last_obs)

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
    return df_to_dict(circ.env.sizing)

def last_action(circ: CircusEnv) -> dict[int, dict[str, float]]:
    """
    Get the last action that was taken. Will be same as sizing if
    `space == 'geom'` otherwise it will be INPUTS.
    """
    return df_to_dict(circ.env.last_obs[circ.env.input_parameters]) \
                if all(i in circ.env.last_obs for i in circ.env.input_parameters) \
                else current_sizing(circ)

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

def num_steps(circ: CircusEnv) -> dict[int, float]:
    """
    Number of steps per environment.
    """
    return dict(enumerate(circ.env.steps.tolist()))
