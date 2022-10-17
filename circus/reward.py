""" Reward Functions """

import operator
from typing import Any, List, Optional, Type, Union, Callable
import numpy as np

def dummy_reward(observation: np.ndarray) -> np.ndarray:
    """
    Default reward function for non-goal environments (v1).
    Arguments:
        - `observation`
    Returns:
        - `reward`
    """
    return np.sum(observation['observation'], axis = 1)

def binary_reward( predicate: list[Callable], observation: dict[str, np.ndarray]
                 , ) -> np.ndarray:
    """
    Default reward function for goal environments (v0).
    Arguments:
        - `predicate`, `observation`
    Returns:
        - `reward` in {-1;0}
    """
    desired_goal  = observation['desired_goal']
    achieved_goal = observation['achieved_goal']

    return np.all( np.stack([ p(a,d) for p,a,d in zip( predicate
                                                     , list(achieved_goal.T)
                                                     , list(desired_goal.T))
                            ]).T
                 , axis = 1 ) - 1.0

def goal_predicate(parameters: list[str]) -> list[Callable]:
    """
    List of default predicates for achived / desired goal comparison:
        - `lambda achived desired: achived <operator> desired`
    """
    preds = { 'area':        operator.le # Area
            , 'a_0':         operator.ge # Gain
            , 'cmrr':        operator.ge # Common Mode Rejection Ration
            , 'cof':         operator.ge # Cross over Frequency
            , 'gm':          operator.ge # Gain Margin
            , 'i_out_max':   operator.ge # Maximum Output Current
            , 'i_out_min':   operator.ge # Minimum Output Current
            , 'idd':         operator.le # Current Consumption
            , 'iss':         operator.le # Current Consumption
            , 'os_f':        operator.ge # Slew Rate Overswing Falling
            , 'os_r':        operator.ge # Slew Rate Overswing Rising
            , 'pm':          operator.ge # Phase Margin
            , 'psrr_n':      operator.ge # Power Supply Rejection Ratio -
            , 'psrr_p':      operator.ge # Power Supply Rejection Ratio +
            , 'sr_f':        operator.ge # Slew Rate Falling
            , 'sr_r':        operator.ge # Slew Rate Rising
            , 'ugbw':        operator.ge # Unity Gain Bandwidth Product
            , 'v_ih':        operator.ge # Input Voltage High
            , 'v_il':        operator.le # Input Voltage Low
            , 'v_oh':        operator.ge # Ouput Voltage High
            , 'v_ol':        operator.le # Ouput Voltage Low
            , 'vn_100Hz':    operator.le # Output-referred noise density @ 100Hz
            , 'vn_100kHz':   operator.le # Output-referred noise density @ 100kHz
            , 'vn_10Hz':     operator.le # Output-referred noise density @ 10Hz
            , 'vn_10kHz':    operator.le # Output-referred noise density @ 10kHz
            , 'vn_1Hz':      operator.le # Output-referred noise density @ 1Hz
            , 'vn_1kHz':     operator.le # Output-referred noise density @ 1kHz
            , 'voff_stat':   operator.le # Statistical Offset
            , 'voff_syst':   operator.le # Systematic Offset
            , }
    return [preds[p] for p in parameters]
