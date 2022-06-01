### Miller Amplifier (OP1)

![op1](https://raw.githubusercontent.com/matthschw/ace/main/figures/op1.png)

Available via `circus` constructor with `circus:op1-<tech>-<space>-<variant>`.

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
gym.spaces.Box( low   = -np.inf
              , high  = np.inf
              , shape = (len(obs_filter), )
              , dtype = np.float32
              , )

```

Where `obs_filter` can be
- `'perf'` by default = `(23,)`
- `'all'` = `(159,)`
- `[...]` = `len`

#### Action Space 

| Variant | Shape    | Parameters                                                                                                                                                   |
|---------|----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `elec`  | `(10, )` | `['MNCM1R:gmoverid', 'MPCM2R:gmoverid', 'MPCS1:gmoverid', 'MND1A:gmoverid', 'MNCM1R:fug', 'MPCM2R:fug', 'MPCS1:fug', 'MND1A:fug', 'MNCM1A:id', 'MNCM1B:id']` |
| `geom`  | `(19, )` | `['Wres', 'Mcap', 'Wcs', 'Wd', 'Lres', 'Wcap', 'Mcm13', 'Mcm12', 'Md', 'Lcm2', 'Ld', 'Wcm2', 'Wcm1', 'Mcm11', 'Mcm22', 'Mcs', 'Lcs', 'Mcm21', 'Lcm1']`       |

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
              , shape = (19,)
              , dtype = np.float32
              , )
```

