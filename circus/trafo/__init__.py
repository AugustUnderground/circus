""" Design Space Transformations """

from typing import Any, List, Optional, Type, Union, Callable
import numpy as np
import pandas as pd

from circus.trafo import mil
from circus.trafo import sym
from circus.trafo import fca
from circus.trafo import rfa

def transformation(ckt_id: str) -> Callable:
    """ Get transformation function for a given ckt id """
    err_msg = f'No Transformation function for {ckt_id} available'
    return { 'mil': mil.transform
           , 'sym': sym.transform
           , 'fca': fca.transform
           , 'rfa': rfa.transform
           , }.get(ckt_id, NotImplementedError(err_msg))

def electric_identifiers(ckt_id: str) -> [str]:
    """ Get Electric Design Parameters for a given ckt id """
    err_msg = f'No Input Parameters for {ckt_id} available'
    return { 'mil': mil.INPUTS
           , 'sym': sym.INPUTS
           , 'fca': fca.INPUTS
           , 'rfa': rfa.INPUTS
           , }.get(ckt_id, NotImplementedError(err_msg))

def electric_unscaler(ckt_id: str) -> Callable:
    """ Min-Max scaler for given ckt id and PDK """
    err_msg = f'No Scaler for {ckt_id} available'
    x_min,x_max,gm,fm,im = { 'mil': mil.unscaler()
                           , 'sym': sym.unscaler()
                           , 'fca': fca.unscaler()
                           , 'rfa': rfa.unscaler()
                           , }.get(ckt_id, NotImplementedError(err_msg))

    def unscale(x: np.ndarray) -> np.ndarray:
        y_ = np.clip( x_min + (((x + 1.0) / 2.0) * (x_max - x_min))
                    , x_min, x_max )

        y = (y_ * gm) + ((10.0 ** (y_ * fm)) * fm) + (y_ * 1.0e-6 * im)

        return y

    return unscale

def performance_scale( ckt_id: str, constraints: dict
                     ) -> (dict[str,float], dict[str,float]):
    """ Return performance scaling dicts (min,max) """
    err_msg = f'No Performance Scale for {ckt_id} available'
    return { 'mil': mil.output_scale
           , 'sym': sym.output_scale
           , 'fca': fca.output_scale
           , 'rfa': rfa.output_scale
           , }.get(ckt_id, NotImplementedError(err_msg)
                  )(constraints)

def reference_goal( ckt_id: str, constraints: dict
                  ) -> pd.DataFrame:
    """ Curated Refernce goal for operational amplifier """
    err_msg = f'No Reference Goal for {ckt_id} available'
    goal    = { 'mil': mil.reference_goal
              , 'sym': sym.reference_goal
              , 'fca': fca.reference_goal
              , 'rfa': rfa.reference_goal
              , }.get(ckt_id, NotImplementedError(err_msg)
                     )(constraints)
    return pd.DataFrame.from_dict({k: [v] for k,v in goal.items()})
