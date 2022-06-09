""" Circus Utility Functions """

from typing import Any, List, Optional, Type, Union, Callable, Tuple
import numpy as np

from .trafo import *

def add_noise(x: np.array, η: float = 0.01) -> np.array:
    """Add some gaussian noise
    Arguments:
        `x`: Input
        `η`: Standard Deviation
    Returns:
        `y`: `x` with noise `η`
    """
    d = x.shape
    μ = np.ones(d)
    σ = np.full(d, η)
    ε = np.random.normal(μ, σ)
    return x * ε

def goal_generator( kind: str, reference: np.ndarray, num_envs: int = 1
                  ) -> Callable:
    """
    Returns a goal generator function
    Arguments:
        `kind`:
            - 'noisy': Add noise to reference goal
            - 'random': Choose a random goal between reference
            - 'fix': Goal remains the same
        `reference`: Must be of shape (num_envs, len(goal_filter)) for 'noisy'
                     and (2, len(goal_filter)) for 'random'. In case of random,
                     `reference[0] == min` and `reference[1] == max` for
                     generating random values in range.
    """
    return ( (lambda : add_noise(reference))
             if kind == 'noisy' else
             (lambda : np.random.uniform( *reference
                                        , size = ( num_envs
                                                 , reference.shape[1] )
                                        , ))
             if kind == 'random' else
             (lambda : reference)
             if kind == 'fix' else
             NotImplementedError(f'Goal kind {kind} not implemented.') )

def filter_results( filter_ids: list[str], results: dict[int, dict[str, float]]
                  ) -> np.ndarray:
    """
    Filter a set of keys from nested dict. Intended to filter observations and
    goal states obtained from ACE. Returns a numpy array where 0th dimension is
    the number of environments and the 1st dimension is `len(filter_ids)`.
    """
    return np.vstack([ np.array([ results[i][k] for k in filter_ids ])
                       for i in sorted(list(results.keys())) ])

def geometric_unscaler(constraints: dict) -> Callable:
    """
    Unscale action ∈ [-1.0;1.0] into real widths and lengths given
    constraints obtained from ACE.
    Returns a scaler function: `scaler :: np.ndarray -> np.ndarray`
    """
    x_min = np.array([ v['min'] for _,v in sorted( constraints.items()
                                                 , key = lambda kv: kv[0] )
                       if v['sizing'] ])
    x_max = np.array([ v['max'] for _,v in sorted( constraints.items()
                                                 , key = lambda kv: kv[0] )
                       if v['sizing'] ])

    return (lambda x: x_min + ( ((np.vstack(x) + 1.0) / 2.0) * (x_max - x_min)))

def performance_scaler( ace_id: str, ace_backend: str, constraints: dict
                      , performance_ids: [str] ) -> Tuple[Callable, Callable]:
    """
    Scale/Unsclae performance obtained from ACE as specified in the
    corresponding `trafo` module, s.t. ∈ [-1.0;1.0].
    Returns a scaler and unscaler funciton:
        `scaler   :: np.ndarray -> np.ndarray`
        `unscaler :: np.ndarray -> np.ndarray`
    **Note**: Since the scaling uses log10, it's a destructive operation,
    unscaling won't work.
    """
    x_min_d, x_max_d = performance_scale(ace_id, ace_backend, constraints)

    abs_msk = np.array([ (pp in [ 'A', 'cof', 'gm', 'i_out_max', 'i_out_min'
                                , 'pm', 'sr_f', 'sr_r', 'ugbw' , 'voff_stat'
                                , 'voff_sys', 'vn_1Hz', 'vn_10Hz' , 'vn_100Hz'
                                , 'vn_1kHz', 'vn_10kHz', 'vn_100kHz'
                                , 'idd', 'iss' ] )
                          for pp in performance_ids ])

    log_msk = np.array([ (pp in [ 'A', 'cof', 'i_out_max', 'i_out_min'
                                , 'sr_f', 'sr_r', 'ugbw', 'voff_stat'
                                , 'voff_sys', 'vn_1Hz', 'vn_10Hz', 'vn_100Hz'
                                , 'vn_1kHz', 'vn_10kHz', 'vn_100kHz'
                                , 'idd', 'iss'])
                          for pp in performance_ids ])

    scl_msk = np.array([pp in list(x_min_d.keys()) for pp in performance_ids])

    x_min   = np.array([ x_min_d[pp] for pp in performance_ids
                                     if  pp in x_min_d.keys() ])
    x_max   = np.array([ x_max_d[pp] for pp in performance_ids
                                     if  pp in x_max_d.keys() ])

    def scaler(x: np.ndarray) -> np.ndarray:
        a            = np.abs(x * abs_msk) + (x * ~abs_msk)
        l            = np.log10( a * log_msk
                               , where = (a * log_msk) > 0.0
                               ) + (a * ~log_msk)
        x_           = np.clip(l[:,scl_msk], x_min, x_max)
        y_           = 2.0 * (x_ - x_min) / (x_max - x_min) - 1.0
        y            = x.copy()
        y[:,scl_msk] = x_
        return y

    def unscaler(y: np.ndarray) -> np.ndarray:
        x_            = y.copy()
        x_[:,scl_msk] = ((y[:,scl_msk] + 1.0) / 2.0) * (x_max - x_min) + x_min
        x             = np.power( 10.0, x_ * log_msk
                                , where = (x_ * log_msk) > 0.0
                                ) + (x_ * ~log_msk)
        return x

    return (scaler, unscaler)
