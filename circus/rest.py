from argparse import ArgumentParser
from collections import namedtuple
from collections.abc import Iterable

import numpy as np
import hace as ac
import gym
import circus

parser = ArgumentParser()
parser.add_argument( "--host", type = str, default = "localhost"
                   , help = "Host address")
parser.add_argument( "-p", "--port", type = int, default = "6006"
                   , help = "Server Port")
parser.add_argument( "-e", "--env", type = str, default = "op2"
                   , help = "ACE Environment ID, see Circus doc for what's available")
parser.add_argument( "-s", "--space", type = str, default = "elec"
                   , help = "Circus Action Space, see Circus doc for what's available")
parser.add_argument( "-v", "--var", type = int, default = "0"
                   , help = "Circus Environment variant, see Circus doc for what's available")
parser.add_argument( "-n", "--num", type = int, default = 1
                   , help = "Number of Pooled Envs")
parser.add_argument( "--pdk", type = str, default = "xh035"
                   , help = "ACE backend, see Circus doc for what's available")

CircusEnv = namedtuple("Environment", "env ace_id backend space variant num_envs")

def make_env( ace_id: str, backend: str, space: str, variant: int
            , num_envs: int, num_steps: int = 50
            ) -> CircusEnv:
    target_filter = ["a_0", "ugbw", "pm", "voff_stat", "cmrr", "psrr_p", "A"]
    env_name      = f"circus:{ace_id}-{backend}-{space}-v{variant}"
    env           = circus.make( env_name, n_envs = num_envs
                               , num_steps = num_steps
                               , goal_ids = target_filter
                               , )
    return CircusEnv(env, ace_id, backend, space, variant, num_envs)

def restart(env: CircusEnv) -> CircusEnv:
    circ, ace_id, backend, space, variant, num_envs = env
    return make_env(ace_id, backend, space, variant, num_envs, circ.num_steps)

def reset(circ: CircusEnv, done_mask = None, restart_count = 0) -> np.ndarray:
    obs = circ.env.reset(done_mask = done_mask)
    return { n: { 'observation':   obs['observation'][n].tolist()
                , 'achieved_goal': obs['achieved_goal'][n].tolist()
                , 'desired_goal':  obs['desired_goal'][n].tolist()
                , } for n in range(circ.num_envs) }

def step(circ: CircusEnv, action: dict, restart_count = 0) -> dict:
    act = np.array([ action[i] for i in sorted(action.keys()) ])
    obs, reward, done, info = circ.env.step(act)
    return { str(n): { 'observation':   obs['observation'][n].tolist()
                     , 'achieved_goal': obs['achieved_goal'][n].tolist()
                     , 'desired_goal':  obs['desired_goal'][n].tolist()
                     , 'reward':        reward[n].item()
                     , 'done':          done[n].item()
                     , 'info':          info[n]
                     , } for n in range(circ.num_envs) }
