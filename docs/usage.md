## Basic Usage

After following the [installation guide](./install.md) diligently `circus` is
ready for use. See `test/example.py` for some code examples and the 
[API Documentation](./circus/index.html) for more details.

```python
import circus
from stable_baselines3 import DDPG

env  = circus.make('circus:op2-xh035-geom-v1')
ddpg = DDPG('MlpPolicy', env, verbose = 1)
ddpg.learn(total_timesteps=10000, log_interval=1)
```

Alternatively, the `gym` registry can be used:

```python
env     = gym.make('circus:op2-xh035-geom-v0')
obs     = env.reset()
a       = np.random.randn(env.action_space.shape[0])
o,r,d,i = env.step(a)
```

The `circus.make` constructor accepts several optional arguments.

```python
# OP2 GoalEnv in xh035 with electric design space
env = circus.make( 'circus:op2-xh035-elec-v0'
                 , n_envs: int                      = 1       # Number of environemts
                 , num_steps: int                   = 50      # Maximum number of steps
                 , seed: int                        = 666     # Random Seed for all Environments
                 , obs_filter: Union[str,List[str]] = 'perf'  # 'perf' | 'all' | [str]
                 , goal_filter: [str]               = None    # List of goal parameters ⊂ `obs_filter`
                 , goal_preds: [Callable]           = None    # Goal predicates
                 , reward_fn: Callable              = binary_reward | dummy_reward # A custom reward function
                 , scale_observation: bool          = True    # Scale observations ∈ [-1.0; 1.0]
                 , auto_reset: bool                 = False   # Automatically Reset when done
                 , )
```

`n_envs`: Number of parallel Environments, should not be more than `nproc`.

`num_steps`: Number of steps per Episodes before goal should be reached.
Otherwise Terminal flag will be set.

`seed`: Random seed for all Environments.

`obs_filter`: Can be either the string `'all'`, for everything ACE has to
offer, the string `'perf'` for only the performance parameters, or a list of
strings with the desired keys in the performance dict obtained from ACE.

`goal_filter`: Is the same as `obs_filter = 'perf'` by default, should be a
subset of `obs_filter`.

`goal_preds`: The goal predicates are a list of operators, which will be called
to determine whether the goal was reached: `performance <operator> goal`.

`reward_fn`: A custom reward function can be passed to the environment. By
default it is `binary_reward` for GoalEnvs (`v0`) and `dummy_reward` for
Non-GoalEnvs (`v1`). See the following subsection for further details.

`scale_observation`: Whether the observations should be scaled to be _roughly_
∈ [-1.0;1.0]. This is based on an estimation and is therefore not 100%
reliable.

#### Custom Reward Function

A custom reward function should be of the following form:

```python
def reward (observation: dict[str, np.ndarray]) -> np.ndarray:
    r = np.random.randn(1)
    return r
```

Where `observation` is a dictionary, with at least one field named
`'observation'` for `VecEnv`s and the fields `'observation'`, `'achieved_goal'`
and `'desired_goal'` for `GoalEnv`s.

### Environment ID Composition

`circus` IDs have a specific structure: `circus:<id>-<pdk>-<space>-v<variant>'`

#### id

The `id` field is linked to the ACE id as shown in the
[availability table](./index.md) and the Table of Contents.

#### pdk

Same goes for the `pdk` field, it is linked to the available ACE backends.

#### space

The `space` field denotes the action space of the agent.

| Space  | Description                           |
|--------|---------------------------------------|
| `elec` | Action space in the electric domain.  |
| `geom` | Action space in the geometric domain. |

#### variant

The variants `v#` define the shape of the observation space

| Variant | Description                  |
|---------|------------------------------|
| `v0`    | `GoalEnv` with `Dict` space. |
| `v1`    | `VecEnv`  with `Box` space.  |
