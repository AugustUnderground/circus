### Amplifier with Wideswing Current Mirror (OP8)

![op8](https://raw.githubusercontent.com/matthschw/ace/main/figures/op8.png)

Available via `circus` constructor with `circus:op8-<tech>-<space>-<variant>`.

#### Observation Space

By default, the `observation` space is set to `'perf'` via the `obs_filter`
kwarg. If it is set to `'all'` the shape will be `(225,)` instead. Otherwise it
will be the length of the given list. Same goes for the goal space.

```python
# v0
gym.spaces.Dict({ 'observation':   Box( -np.Inf, np.Inf, (29,))
                , 'achieved_goal': Box( -np.Inf, np.Inf, (23,))
                , 'desired_goal':  Box( -np.Inf, np.Inf, (23,))
                , })

# v1
gym.spaces.Box( low   = -np.inf
              , high  = np.inf
              , shape = (29,)
              , dtype = np.float32
              , )

```

#### Action Space 

| Variant | Shape    | Parameters                                                                                                                                                       |
|---------|----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `elec`  | `(14, )` | `['MNCM11:gmoverid', 'MPCM221:gmoverid', 'MNCM31:gmoverid', 'MND11:gmoverid', 'MNCM11:fug', 'MPCM221:fug', 'MNCM31:fug', 'MND11:fug', 'MNCM12:id', 'MNCM32:id']` |
| `geom`  | `(22, )` | `['Wd', 'Mcm12', 'Md', 'Lcm2', 'Ld', 'Wcm2', 'Lcm3', 'Wcm1', 'Wcm3', 'Mcm11', 'Mcm22', 'Mcm21', 'Mcm32', 'Mcm31', 'Lcm1']`                                       |

The parameter identifiers can be obtained through the `input_parameters` field
of the environment.

```python
# elec
gym.spaces.Box( low   = -1.0
              , high  = 1.0
              , shape = (14,)
              , dtype = np.float32
              , )

# geom
gym.spaces.Box( low   = -1.0
              , high  = 1.0
              , shape = (22,)
              , dtype = np.float32
              , )
```

