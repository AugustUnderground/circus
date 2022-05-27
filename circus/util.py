""" Utility Functions """

from typing import Any, List, Optional, Type, Union, Callable
import numpy as np

def add_noise(x: np.array, ε: float = 0.1) -> np.array:
    """ Add some gaussian noise """
    d = x.shape
    return (x + (x * np.random.normal(np.ones(d), np.full(d, ε))))

def geometric_unscaler(constraints: dict) -> Callable:
    """ Unscale action ∈ [-1.0;1.0] into real action """

    x_min = np.array([ v['min'] for _,v in sorted( constraints.items()
                                                 , key = lambda kv: kv[0] )
                       if v['sizing'] ])
    x_max = np.array([ v['max'] for _,v in sorted( constraints.items()
                                                 , key = lambda kv: kv[0] )
                       if v['sizing'] ])

    return (lambda x: x_min + ( ((np.vstack(x) + 1.0) / 2.0) * (x_max - x_min)))
