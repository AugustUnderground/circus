import time
from memory_profiler import profile
import circus
import numpy as np

@profile
def profile_circus(env):
    for n in range(int(1e8)):
        if n % 50:
            env.reset()
        act     = np.vstack([env.action_space.sample()] * env.num_envs)
        o,r,d,i = env.step(act)

def main() -> int:
    n       = 5
    env     = circus.make('circus:op2-xh035-elec-v0', n_envs = n)
    profile_circus(env)
    return 0

if __name__ == '__main__':
    main()
