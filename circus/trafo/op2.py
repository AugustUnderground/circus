""" Agnostic Design Space Transforation for OP2: Symmetrical Amplifier """

from fractions import Fraction
from typing import Any, List, Optional, Type, Union, Callable
import numpy as np

from ..prim import PrimitiveDevice

INPUTS: [str] = [ 'MNCM11:gmoverid', 'MPCM221:gmoverid', 'MNCM31:gmoverid', 'MND11:gmoverid'
                , 'MNCM11:fug',      'MPCM221:fug',      'MNCM31:fug',      'MND11:fug'
                , 'MNCM12:id',       'MNCM32:id' ]

def transform( constraints: dict, nmos: PrimitiveDevice, pmos: PrimitiveDevice
             , gmid_cm1: float, gmid_cm2: float, gmid_cm3: float, gmid_dp1: float
             , fug_cm1: float,  fug_cm2: float,  fug_cm3: float,  fug_dp1: float
             , i1: float, i2: float ) -> dict[str, float]:
    """ Transforation for OP2 """

    i0      = constraints.get('i0', {}).get('init', 3e-6)
    vdd     = constraints.get('vsup', {}).get('init', 3.3)

    M1_lim  = int(constraints.get('Mcm12', {}).get('max', 42))
    M2_lim  = int(constraints.get('Mcm22', {}).get('max', 42))

    M1      = Fraction(i0       / i1).limit_denominator(M1_lim)
    M2      = Fraction(i1 / 2.0 / i2).limit_denominator(M2_lim)

    Mcm11   = max(M1.numerator, 1)
    Mcm12   = max(M1.denominator, 1)
    Mcm21   = max(M2.numerator, 1)
    Mcm22   = max(M2.denominator, 1)

    Mdp01   = constraints.get('Md'   , {}).get('init', 2)
    Mcm31   = constraints.get('Mcm31', {}).get('init', 2)
    Mcm32   = constraints.get('Mcm32', {}).get('init', 2)

    cm1_in  = np.array([[gmid_cm1, fug_cm1,  (vdd / 4.0),         0.0 ]])
    cm2_in  = np.array([[gmid_cm2, fug_cm2, -(vdd / 3.0),         0.0 ]])
    cm3_in  = np.array([[gmid_cm3, fug_cm3,  (vdd / 4.0),         0.0 ]])
    dp1_in  = np.array([[gmid_dp1, fug_dp1,  (vdd / 3.0), -(vdd / 4.0)]])

    cm1_out = nmos.predict(cm1_in)[0]
    cm2_out = pmos.predict(cm2_in)[0]
    cm3_out = nmos.predict(cm3_in)[0]
    dp1_out = nmos.predict(dp1_in)[0]

    Lcm1    = cm1_out[1]
    Lcm2    = cm2_out[1]
    Lcm3    = cm3_out[1]
    Ldp1    = dp1_out[1]

    Wcm1    = i0       / cm1_out[0] / Mcm11
    Wcm2    = i1 / 2.0 / cm2_out[0] / Mcm21
    Wcm3    = i2       / cm3_out[0] / Mcm31
    Wdp1    = i1 / 2.0 / dp1_out[0] / Mdp01

    sizing  = { 'Ld': Ldp1,  'Lcm1':  Lcm1,  'Lcm2':  Lcm2,  'Lcm3':  Lcm3
              , 'Wd': Wdp1,  'Wcm1':  Wcm1,  'Wcm2':  Wcm2,  'Wcm3':  Wcm3
              , 'Md': Mdp01, 'Mcm11': Mcm11, 'Mcm21': Mcm21, 'Mcm31': Mcm31
                           , 'Mcm12': Mcm12, 'Mcm22': Mcm22, 'Mcm32': Mcm32
              , }

    return sizing

def unscaler(ace_backend: str) -> tuple[ np.ndarray, np.ndarray, np.ndarray
                                       , np.ndarray, np.ndarray]:
    """ Unscale function for a given PDK """
    x_min = np.array([5.0,  5.0,  5.0,  5.0,  6.0, 6.0, 6.0, 6.0, 1.0,  3.0])
    x_max = np.array([15.0, 15.0, 15.0, 15.0, 9.0, 9.0, 9.0, 9.0, 6.0, 15.0])
    gm    = np.array([(i in range(0,4))  for i in range(10)])
    fm    = np.array([(i in range(4,8))  for i in range(10)])
    im    = np.array([(i in range(8,10)) for i in range(10)])
    return (x_min, x_max, gm, fm, im)

def output_scale( constraints: dict, ace_backend: str
                ) -> tuple[dict[str, float], dict[str,float]]:
    vdd   = constraints.get('vsup', {}).get('init', 3.3)
    x_min = { 'a_0'         : 25.0
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
    x_max = { 'a_0'         : 70.0
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
    return (x_min, x_max)
