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

def filter_results( filter_ids: [str], results: dict[int, dict[str, float]]
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
    """
    err_msg = f'No Performance Scale for {ace_id} available'
    x_min_d, x_max_d = { 'op1': op1.output_scale
                       , 'op2': op2.output_scale
                       , 'op8': op8.output_scale
                       , }.get( ace_id, NotImplementedError(err_msg)
                              )(constraints, ace_backend)

    abs_msk = np.array([ (pp in [ 'A', 'cof', 'gm', 'i_out_max', 'i_out_min'
                                , 'pm', 'sr_f', 'sr_r', 'ugbw' , 'voff_stat'
                                , 'voff_sys', 'vn_1Hz', 'vn_10Hz' , 'vn_100Hz'
                                , 'vn_1kHz', 'vn_10kHz', 'vn_100kHz'] )
                          for pp in performance_ids ])

    log_msk = np.array([ (pp in [ 'A', 'cof', 'i_out_max', 'i_out_min'
                                , 'sr_f', 'sr_r', 'ugbw', 'voff_stat'
                                , 'voff_sys', 'vn_1Hz', 'vn_10Hz', 'vn_100Hz'
                                , 'vn_1kHz', 'vn_10kHz', 'vn_100kHz'])
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
        y_           = 2.0 * (l[:,scl_msk] - x_min) / (x_max - x_min) - 1.0
        y            = x.copy()
        y[:,scl_msk] = y_
        return y

    def unscaler(y: np.ndarray) -> np.ndarray:
        y_           = ((y + 1.0) / 2.0) * (x_max - x_min) + x_min
        p            = np.power( 10.0, y_ * log_msk
                               , where = (y_ * log_msk) > 0.0
                               ) + (y_ * ~log_msk)
        x            = y.copy()
        x[:,scl_msk] = p
        return x

    return (scaler, unscaler)
