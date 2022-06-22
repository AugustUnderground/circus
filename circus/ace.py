""" ACE Utilities """

import operator
from typing import Any, List, Optional, Type, Union, Callable

def backend_id(pdk: str) -> str:
    """
    ACE Backend ID Generator.
    """
    err_msg = f'No ACE Backend found for {pdk}'
    return (pdk + '-3V3' if pdk == 'xh035'  else
            pdk + '-1V8' if pdk == 'xh018'  else
            pdk + '-1V8' if pdk == 'xt018'  else
            pdk + '-1V8' if pdk == 'sky130' else
            NotImplementedError(err_msg))

def goal_predicate(parameters: list[str]) -> list[Callable]:
    """
    List of default predicates for achived / desired goal comparison:
        lambda achived desired: ...
    """
    preds = { 'A':           operator.le # Area
            , 'a_0':         operator.ge # Gain
            , 'cmrr':        operator.ge # Common Mode Rejection Ration
            , 'cof':         operator.ge # Cross over Frequency
            , 'gm':          operator.ge # Gain Margin
            , 'i_out_max':   operator.ge # Maximum Output Current
            , 'i_out_min':   operator.ge # Minimum Output Current
            , 'idd':         operator.le # Current Consumption
            , 'iss':         operator.le # Current Consumption
            , 'overshoot_f': operator.ge # Slew Rate Overswing Falling
            , 'overshoot_r': operator.ge # Slew Rate Overswing Rising
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
            , 'voff_sys':    operator.le # Systematic Offset
            , }
    return [preds[p] for p in parameters]
