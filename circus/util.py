""" Circus Utility Functions """

import os
import errno
import yaml
from typing import Any, List, Optional, Type, Union, Callable, Tuple, Iterable
from functools import partial
import numpy as np
import pandas as pd
import serafin as sf
import pyspectre as ps

from .trafo import *

def df_to_dict(df: pd.DataFrame) -> dict[int, dict[str, float]]:
    """ Convert a dataframe to a dictionary """
    return { row.Index: { k: np.nan_to_num(v, nan = 0.0, posinf = 0.0, neginf = 0.0)
                          for k,v in row._asdict().items() if (k != 'Index') }
             for row in df.itertuples() }

def add_noise(x: np.array, η: float = 0.01) -> np.array:
    """Add some gaussian noise
    Arguments:
        - `x`: Input
        _ `η`: Standard Deviation
    Returns:
        _ `y`: `x` with noise `η`
    """
    d = x.shape
    μ = np.ones(d)
    σ = np.full(d, η)
    ε = np.random.normal(μ, σ)
    return x * ε

def goal_generator( kind: str, reference: pd.DataFrame
                  ) -> Callable:
    """
    Returns a goal generator function
    Arguments:
        - `kind`:
            + 'noisy': Add noise to reference goal
            + 'random': Choose a random goal between reference
            + 'fix': Goal remains the same
        - `reference`: Must be of shape (num_envs, len(goal_filter)) for 'noisy'
                       and (2, len(goal_filter)) for 'random'. In case of random,
                       `reference[0] == min` and `reference[1] == max` for
                       generating random values in range.
    """
    return ( (lambda : reference.apply(add_noise))
             if kind == 'noisy' else
             (lambda : pd.DataFrame( np.random.uniform( *reference.values
                                                      , size = ( reference.shape[0]
                                                               , reference.shape[1] )
                                                      , )
                                   , columns = reference.columns ))
             if kind == 'random' else
             (lambda : reference)
             if kind == 'fix' else
             NotImplementedError(f'Goal kind {kind} not implemented.') )

def filter_results( filter_ids: Iterable[str], results: pd.DataFrame
                  ) -> pd.DataFrame:
    """
    Extracts given columns for data Frame and makes sure there are no NaNs.
    """
    n2n = partial(np.nan_to_num, nan = 0.0, posinf = 0.0, neginf = 0.0)
    return results[filter_ids].apply(n2n)

def geometric_unscaler( constraints: dict[str, dict[str, float]]
                      , geom_params: Iterable[str]
                      ) -> Callable:
    """
    Unscale action ∈ [-1.0;1.0] into real widths and lengths given
    constraints obtained from serafin.
    Returns a scaler function: `scaler :: np.ndarray -> np.ndarray`
    """
    x_min = np.array([ ( constraints['length']['min'] if g.startswith('L') else
                         constraints['width']['min'] if g.startswith('W') else
                         1.0 ) for g in geom_params ])
    x_max = np.array([ ( constraints['length']['max'] if g.startswith('L') else
                         constraints['width']['max'] if g.startswith('W') else
                         40.0 ) for g in geom_params ])

    return (lambda x: x_min + ( ((np.vstack(x) + 1.0) / 2.0) * (x_max - x_min)))

def performance_scaler( ckt_id: str, constraints: dict
                      , performance_ids: Iterable[str]
                      ) -> Tuple[Callable, Callable]:
    """
    Scale/Unscale performance obtained from serafin as specified in the
    corresponding `trafo` module, s.t. ∈ [-1.0;1.0].
    Returns a scaler and unscaler funciton:
        - `scaler   :: np.ndarray -> np.ndarray`
        - `unscaler :: np.ndarray -> np.ndarray`
    **Note**: Since the scaling uses log10, it's a destructive operation,
    unscaling might result in the wrong sign.
    """
    x_min_d, x_max_d = performance_scale(ckt_id, constraints)

    abs_msk = np.array([ (pp in [ 'area', 'cof', 'gm', 'i_out_max', 'i_out_min'
                                , 'pm', 'sr_f', 'sr_r', 'ugbw' , 'voff_stat'
                                , 'voff_sys', 'vn_1Hz', 'vn_10Hz' , 'vn_100Hz'
                                , 'vn_1kHz', 'vn_10kHz', 'vn_100kHz'
                                , 'idd', 'iss' ] )
                          for pp in performance_ids ])

    log_msk = np.array([ (pp in [ 'area', 'cof', 'i_out_max', 'i_out_min'
                                , 'sr_f', 'sr_r', 'ugbw', 'voff_stat'
                                , 'voff_syst', 'vn_1Hz', 'vn_10Hz', 'vn_100Hz'
                                , 'vn_1kHz', 'vn_10kHz', 'vn_100kHz'
                                , 'idd', 'iss' ])
                          for pp in performance_ids ])

    scl_msk = np.array([pp in list(x_min_d.keys()) for pp in performance_ids])

    x_min   = np.array([ x_min_d[pp] for pp in performance_ids
                                     if  pp in x_min_d.keys() ])
    x_max   = np.array([ x_max_d[pp] for pp in performance_ids
                                     if  pp in x_max_d.keys() ])

    def scaler(x: np.ndarray) -> np.ndarray:
        a            = (np.abs(x) * abs_msk) + (x * ~abs_msk)
        l            = (np.log10(a, where = (a * log_msk) > 0.0) * log_msk
                       ) + (a * ~log_msk)
        x_           = np.clip(l[:,scl_msk], x_min, x_max)
        y_           = 2.0 * (x_ - x_min) / (x_max - x_min) - 1.0
        y            = x.copy()
        y[:,scl_msk] = y_

        return y

    def unscaler(y: np.ndarray) -> np.ndarray:
        x_            = y.copy()
        x_[:,scl_msk] = ((y[:,scl_msk] + 1.0) / 2.0) * (x_max - x_min) + x_min
        x = (10 ** (x_ * log_msk)) * log_msk + (x_ * ~log_msk)

        return x

    return (scaler, unscaler)
