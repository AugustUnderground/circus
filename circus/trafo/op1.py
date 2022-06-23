"""
Agnostic Design Space Transforation for OP1: Miller Operational Amplifier

`INPUTS`
-------
Input parameters are 
[ 'MNCM1R:gmoverid', 'MPCM2R:gmoverid', 'MPCS1:gmoverid', 'MND1A:gmoverid'
, 'MNCM1R:fug',      'MPCM2R:fug',      'MPCS1:fug',      'MND1A:fug'
, 'MNCM1A:id', 'MNCM1B:id' ]
"""

from fractions import Fraction
from typing import Any, List, Optional, Type, Union, Callable
import numpy as np

from ..prim import PrimitiveDevice

INPUTS: [str] = [ 'MNCM1R:gmoverid', 'MPCM2R:gmoverid', 'MPCS1:gmoverid', 'MND1A:gmoverid'
                , 'MNCM1R:fug',      'MPCM2R:fug',      'MPCS1:fug',      'MND1A:fug'
                #'RC:res' 'CC:cap'
                , 'MNCM1A:id', 'MNCM1B:id' ]

def transform( constraints: dict, nmos: PrimitiveDevice, pmos: PrimitiveDevice
             , gmid_cm1: float, gmid_cm2: float, gmid_cs1: float, gmid_dp1: float
             , fug_cm1: float,  fug_cm2: float,  fug_cs1: float,  fug_dp1: float
             #, res: float, cap: float
             , i1: float, i2: float ) -> dict[str, float]:
    """
    Transforation for OP1
    Arguments:
        `constraints`: Design constraints as obtained from ACE.
        `nmos`:     NMOS model of type `PrimitiveDevice`
        `pmos`:     PMOS model of type `PrimitiveDevice`
        `gmid_cm1`: MNCM13:gmoverid
        `gmid_cm2`: MPCM2R:gmoverid
        `gmid_cs1`: MPCS1:gmoverid
        `gmid_dp1`: MND1A:gmoverid
        `fug_cm1`:  MNCM13:fug
        `fug_cm2`:  MPCM2R:fug
        `fug_cs1`:  MPCS1:fug
        `fug_dp1`:  MND1A:fug
        `i1`:       MNCM1A:id
        `i2`:       MNCM1B:id
    """

    #sr      = 2.5e6
    #cl      = constraints.get('cl', {}).get('init', 5e-12)
    #cc      = i1 / sr
    #rc      = (1 / (gmid_cs1 * i2)) * ((cc + cl) / cc)

    i0      = constraints.get('i0',   {}).get('init', 3e-6)
    vdd     = constraints.get('vsup', {}).get('init', 3.3)

    Wres    = constraints.get('Wres', {}).get('init', 2e-6)
    Lres    = constraints.get('Lres', {}).get('init', 113e-6)
    Wcap    = constraints.get('Wcap', {}).get('init', 69e-6)
    Mcap    = constraints.get('Mcap', {}).get('init', 1)

    Mcm21   = constraints.get('Mcm21', {}).get('init', 2)
    Mcm22   = constraints.get('Mcm22', {}).get('init', 2)
    Mdp1    = constraints.get('Md',    {}).get('init', 2)

    M1_lim  = int(constraints.get('Mcm12', {}).get('max', 42))
    M3_lim  = int(constraints.get('Mcm13', {}).get('max', 42))

    Wc_lim  = float(constraints.get('Wcs',   {}).get('max', 150e-6))

    M1      = Fraction(i0 / i1).limit_denominator(M1_lim)
    M3      = Fraction(i0 / i2).limit_denominator(M3_lim)

    Mcm11   = max(M1.numerator, 1)
    Mcm12   = max(M1.denominator, 1)
    Mcm13   = max((M1.numerator * M3.denominator) // max(M3.numerator, 1), 1)

    cm1_in  = np.array([[gmid_cm1, fug_cm1,  (vdd / 4.0),         0.0 ]])
    cm2_in  = np.array([[gmid_cm2, fug_cm2, -(vdd / 3.0),         0.0 ]])
    cs1_in  = np.array([[gmid_cs1, fug_cs1, -(vdd / 2.0),         0.0 ]])
    dp1_in  = np.array([[gmid_dp1, fug_dp1,  (vdd / 3.0), -(vdd / 4.0)]])

    cm1_out = nmos.predict(cm1_in)[0]
    cm2_out = pmos.predict(cm2_in)[0]
    cs1_out = pmos.predict(cs1_in)[0]
    dp1_out = nmos.predict(dp1_in)[0]

    Lcm1    = cm1_out[1]
    Lcm2    = cm2_out[1]
    Lcs1    = cs1_out[1]
    Ldp1    = dp1_out[1]

    Wcm1    = i0       / cm1_out[0] / Mcm11
    Wcm2    = i1 / 2.0 / cm2_out[0] / Mcm21
    Wdp1    = i1 / 2.0 / dp1_out[0] / Mdp1

    Wcs     = i2       / cs1_out[0]
    Mcs1    = np.ceil(Wcs / Wc_lim).item()
    Wcs1    = Wcs / Mcs1

    sizing  = { 'Ld': Ldp1, 'Lcm1':  Lcm1,  'Lcm2':  Lcm2,  'Lcs': Lcs1, 'Lres': Lres
              , 'Wd': Wdp1, 'Wcm1':  Wcm1,  'Wcm2':  Wcm2,  'Wcs': Wcs1, 'Wres': Wres, 'Wcap': Wcap
              , 'Md': Mdp1, 'Mcm11': Mcm11, 'Mcm21': Mcm21, 'Mcs': Mcs1,               'Mcap': Mcap
                          , 'Mcm12': Mcm12, 'Mcm22': Mcm22
                          , 'Mcm13': Mcm13
              , }

    return sizing

def unscaler(ace_backend: str) -> tuple[ np.ndarray, np.ndarray, np.ndarray
                                       , np.ndarray, np.ndarray ]:
    """
    Unscale function [-1.0; 1.0] for a given PDK. Used for scaling actions.
    Arguments:
        `ace_backend`: PDK
    """
    err   = f'No Input Scale for {ace_backend} available'
    x_min = { 'xh035-3V3': np.array([ 5.0, 5.0, 5.0, 5.0
                                    , 6.0, 6.0, 6.0, 6.0
                                    , 10.0, 40.0 ])
            , 'xh018-1V8': np.array([ 5.0, 5.0, 5.0, 5.0
                                    , 6.0, 6.0, 6.0, 6.0
                                    , 10.0, 40.0 ])
            , }.get(ace_backend, NotImplementedError(err))
    x_max = { 'xh035-3V3': np.array([ 15.0, 15.0, 15.0, 15.0
                                    , 9.0, 9.0, 9.0, 9.0
                                    , 30.0, 80.0 ])
            , 'xh018-1V8': np.array([ 15.0, 15.0, 15.0, 15.0
                                    , 9.0, 9.0, 9.0, 9.0
                                    , 30.0, 80.0 ])
            , }.get(ace_backend, NotImplementedError(err))
    gm    = np.array([(i in range(0,4))  for i in range(10)])
    fm    = np.array([(i in range(4,8))  for i in range(10)])
    im    = np.array([(i in range(8,10)) for i in range(10)])
    return (x_min, x_max, gm, fm, im)

def output_scale( constraints: dict, ace_backend: str
                ) -> tuple[dict[str, float], dict[str, float]]:
    """
    Estimated [-1.0;1.0] scaler for the Performance obtained from ACE.
    Arguments:
        `constraints`: Design constraints obtained from ACE.
        `ace_backend`: PDK
    """
    err   = f'No Performance Scale for {ace_backend} available'
    vdd   = constraints.get('vsup', {}).get('init', 3.3)
    x_min = { 'xh035-3V3': { 'a_0'         : 25.0
                           , 'ugbw'        : 5.0
                           , 'pm'          : 0.0
                           , 'gm'          : 0.0
                           , 'sr_r'        : 4.0
                           , 'sr_f'        : 4.0
                           , 'vn_1Hz'      : -10.0
                           , 'vn_10Hz'     : -10.0
                           , 'vn_100Hz'    : -10.0
                           , 'vn_1kHz'     : -10.0
                           , 'vn_10kHz'    : -10.0
                           , 'vn_100kHz'   : -10.0
                           , 'cmrr'        : 70
                           , 'psrr_n'      : 30.0
                           , 'psrr_p'      : 40.0
                           , 'v_il'        : 0.0
                           , 'v_ih'        : 0.0
                           , 'v_ol'        : 0.0
                           , 'v_oh'        : 0.0
                           , 'i_out_min'   : -6.0
                           , 'i_out_max'   : -6.0
                           , 'idd'         : -6.0
                           , 'iss'         : -6.0
                           , 'overshoot_r' : 0.0
                           , 'overshoot_f' : 0.0
                           , 'cof'         : 5.0
                           , 'voff_stat'   : -5.0
                           , 'voff_sys'    : -5.0
                           , 'A'           : -15.0
                           , }
            , 'xh018-1V8': { 'a_0'         : 25.0
                           , 'ugbw'        : 5.0
                           , 'pm'          : 0.0
                           , 'gm'          : 0.0
                           , 'sr_r'        : 4.0
                           , 'sr_f'        : 4.0
                           , 'vn_1Hz'      : -10.0
                           , 'vn_10Hz'     : -10.0
                           , 'vn_100Hz'    : -10.0
                           , 'vn_1kHz'     : -10.0
                           , 'vn_10kHz'    : -10.0
                           , 'vn_100kHz'   : -10.0
                           , 'cmrr'        : 70
                           , 'psrr_n'      : 30.0
                           , 'psrr_p'      : 40.0
                           , 'v_il'        : 0.0
                           , 'v_ih'        : 0.0
                           , 'v_ol'        : 0.0
                           , 'v_oh'        : 0.0
                           , 'i_out_min'   : -6.0
                           , 'i_out_max'   : -6.0
                           , 'idd'         : -6.0
                           , 'iss'         : -6.0
                           , 'overshoot_r' : 0.0
                           , 'overshoot_f' : 0.0
                           , 'cof'         : 5.0
                           , 'voff_stat'   : -5.0
                           , 'voff_sys'    : -5.0
                           , 'A'           : -15.0
                           , }
            , }.get(ace_backend, NotImplementedError(err))
    x_max = { 'xh035-3V3': { 'a_0'         : 70.0
                           , 'ugbw'        : 10.0
                           , 'pm'          : 120.0
                           , 'gm'          : 80.0
                           , 'sr_r'        : 8.0
                           , 'sr_f'        : 8.0
                           , 'vn_1Hz'      : -4.0
                           , 'vn_10Hz'     : -4.0
                           , 'vn_100Hz'    : -4.0
                           , 'vn_1kHz'     : -4.0
                           , 'vn_10kHz'    : -4.0
                           , 'vn_100kHz'   : -4.0
                           , 'cmrr'        : 150.0
                           , 'psrr_n'      : 70.0
                           , 'psrr_p'      : 140.0
                           , 'v_il'        : (2.0 * vdd)
                           , 'v_ih'        : (2.0 * vdd)
                           , 'v_ol'        : (2.0 * vdd)
                           , 'v_oh'        : (2.0 * vdd)
                           , 'i_out_min'   : -3.0
                           , 'i_out_max'   : -3.0
                           , 'idd'         : -3.0
                           , 'iss'         : -3.0
                           , 'overshoot_r' : 130.0
                           , 'overshoot_f' : 130.0
                           , 'cof'         : 9.0
                           , 'voff_stat'   : 0.0
                           , 'voff_sys'    : 0.0
                           , 'A'           : -5.0
                           , }
            , 'xh018-1V8': { 'a_0'         : 70.0
                           , 'ugbw'        : 10.0
                           , 'pm'          : 120.0
                           , 'gm'          : 80.0
                           , 'sr_r'        : 8.0
                           , 'sr_f'        : 8.0
                           , 'vn_1Hz'      : -4.0
                           , 'vn_10Hz'     : -4.0
                           , 'vn_100Hz'    : -4.0
                           , 'vn_1kHz'     : -4.0
                           , 'vn_10kHz'    : -4.0
                           , 'vn_100kHz'   : -4.0
                           , 'cmrr'        : 150.0
                           , 'psrr_n'      : 70.0
                           , 'psrr_p'      : 140.0
                           , 'v_il'        : (2.0 * vdd)
                           , 'v_ih'        : (2.0 * vdd)
                           , 'v_ol'        : (2.0 * vdd)
                           , 'v_oh'        : (2.0 * vdd)
                           , 'i_out_min'   : -3.0
                           , 'i_out_max'   : -3.0
                           , 'idd'         : -3.0
                           , 'iss'         : -3.0
                           , 'overshoot_r' : 130.0
                           , 'overshoot_f' : 130.0
                           , 'cof'         : 9.0
                           , 'voff_stat'   : 0.0
                           , 'voff_sys'    : 0.0
                           , 'A'           : -5.0
                           , }
            , }.get(ace_backend, NotImplementedError(err))
    return (x_min, x_max)
