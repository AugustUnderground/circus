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
        y_ = np.clip( x_min + (((x + 1.0) / 2.0) * (x_max - x_min))
                    , x_min, x_max )

        y = (y_ * gm) + ((10.0 ** (y_ * fm)) * fm) + (y_ * 1.0e-6 * im)

        return y

    return unscale

def performance_scale( ace_id: str, ace_backend: str, constraints: dict
                          ) -> (dict[str,float], dict[str,float]):
    """ Return performance scaling dicts (min,max) """
    err_msg = f'No Performance Scale for {ace_id} available'
    return { 'op1': op1.output_scale
           , 'op2': op2.output_scale
           , 'op8': op8.output_scale
           , }.get(ace_id, NotImplementedError(err_msg)
                  )(constraints, ace_backend)

def reference_goal( ace_id: str, ace_backend: str, constraints: dict
                  ) -> dict[str, float]:
    """ Curated Refernce goal for OP """
    err_msg = f'No Reference Goal for {ace_id} available'
    return { 'op1': op1.reference_goal
           , 'op2': op2.reference_goal
           , 'op8': op8.reference_goal
           , }.get(ace_id, NotImplementedError(err_msg)
                  )(constraints, ace_backend)
