""" Design Space Transformations """

from typing import Any, List, Optional, Type, Union, Callable
import numpy as np

from circus.trafo import op1
from circus.trafo import op2
from circus.trafo import op8

def transformation(ace_id: str) -> Callable:
    """ Get transformation function for a given ace id """
    err_msg = f'No Transformation function for {ace_id} available'
    return { 'op1': op1.transform
           , 'op2': op2.transform
           , 'op8': op8.transform
           , }.get(ace_id, NotImplementedError(err_msg))

def electric_identifiers(ace_id: str) -> [str]:
    """ Get Electric Design Parameters for a given ace id """
    err_msg = f'No Input Parameters for {ace_id} available'
    return { 'op1': op1.INPUTS
           , 'op2': op2.INPUTS
           , 'op8': op8.INPUTS
           , }.get(ace_id, NotImplementedError(err_msg))

def electric_unscaler(ace_id: str, ace_backend: str) -> Callable:
    """ Min-Max scaler for given ACE ID and PDK """
    err_msg = f'No Scaler for {ace_id} available'
    x_min,x_max,gm,fm,im = { 'op1': op1.unscaler(ace_backend)
                           , 'op2': op2.unscaler(ace_backend)
                           , 'op8': op8.unscaler(ace_backend)
                           , }.get(ace_id, NotImplementedError(err_msg))

    def unscale(x: np.ndarray) -> np.ndarray:
        y_ = x_min + (((x + 1.0) / 2.0) * (x_max - x_min))
        y  = (y_ * gm) \
           + np.log10(y_ * fm, where = (y_ * fm) > 0.0) \
           + (y_ * im * 1e-6)
        return y

    return unscale


