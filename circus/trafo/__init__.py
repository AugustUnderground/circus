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

def electric_unscaler(ace_id: str, ace_backend: str) -> tuple[np.array, np.array]:
    """ Min-Max scaler for given ACE ID and PDK """
    err_msg = f'No Scaler for {ace_id} available'
    return { 'op1': op1.unscaler(ace_backend)
           , 'op2': op2.unscaler(ace_backend)
           , 'op8': op8.unscaler(ace_backend)
           , }.get(ace_id, NotImplementedError(err_msg))
