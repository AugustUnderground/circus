### Symmetrical Amplifier (OP2)

![op2](https://raw.githubusercontent.com/matthschw/ace/main/figures/op2.png)

Available via `circus` constructor with `circus:op2-<tech>-<space>-<variant>`.

#### Observation Space

```python
# v0
gym.spaces.Dict({ 'observation':   Box( -np.Inf, np.Inf
                                      , (len(obs_filter),))
                , 'achieved_goal': Box( -np.Inf, np.Inf
                                      , (len(goal_filter),))
                , 'desired_goal':  Box( -np.Inf, np.Inf
                                      , (len(goal_filter),))
                , })

# v1
gym.spaces.Box(low   = -np.inf
              , high  = np.inf
              , shape = (len(obs_filter), )
              , dtype = np.float32
              , )

```

Where `obs_filter` can be
- `'perf'` by default = `(23,)`
- `'all'` = `(194,)`
- `[...]` = `len`

#### Action Space 

| Variant | Shape    | Parameters                                                                                                                                                       |
|---------|----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `elec`  | `(10, )` | `['MNCM11:gmoverid', 'MPCM221:gmoverid', 'MNCM31:gmoverid', 'MND11:gmoverid', 'MNCM11:fug', 'MPCM221:fug', 'MNCM31:fug', 'MND11:fug', 'MNCM12:id', 'MNCM32:id']` |
| `geom`  | `(15, )` | `['Wd', 'Mcm12', 'Md', 'Lcm2', 'Ld', 'Wcm2', 'Lcm3', 'Wcm1', 'Wcm3', 'Mcm11', 'Mcm22', 'Mcm21', 'Mcm32', 'Mcm31', 'Lcm1']`                                       |

The parameter identifiers can be obtained through the `input_parameters` field
of the environment.

```python
# elec
gym.spaces.Box( low   = -1.0
              , high  = 1.0
              , shape = (10,)
              , dtype = np.float32
              , )

# geom
gym.spaces.Box( low   = -1.0
              , high  = 1.0
              , shape = (15,)
              , dtype = np.float32
              , )
```

