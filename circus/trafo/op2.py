""" Agnostic Design Space Transforation for OP2: Symmetrical Amplifier """

from fractions import Fraction
from typing import Any, List, Optional, Type, Union, Callable
import numpy as np

from ..prim import PrimitiveDevice

INPUTS: list[str] = [ 'MNCM11:gmoverid', 'MPCM221:gmoverid', 'MNCM31:gmoverid', 'MND11:gmoverid'
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

    cm1_in  = np.array([[gmid_cm1, fug_cm1,  (vdd / 4.25),         0.00 ]])
    cm2_in  = np.array([[gmid_cm2, fug_cm2, -(vdd / 3.15),         0.00 ]])
    cm3_in  = np.array([[gmid_cm3, fug_cm3,  (vdd / 4.25),         0.00 ]])
    dp1_in  = np.array([[gmid_dp1, fug_dp1,  (vdd / 2.10), -(vdd / 4.85)]])

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
    err   = f'No Input Scale for {ace_backend} available'
    x_min = { 'xh035-3V3': np.array([5.0,  5.0,  5.0,  5.0,  7.0, 7.0, 7.0, 7.0, 1.0,  6.0])
            , 'xh018-1V8': np.array([5.0,  5.0,  5.0,  5.0,  7.0, 7.0, 7.0, 7.0, 1.0,  3.0])
            , }.get(ace_backend, NotImplementedError(err))
    x_max = { 'xh035-3V3': np.array([15.0, 15.0, 15.0, 15.0, 9.0, 9.0, 9.0, 9.0, 9.0, 15.0])
            , 'xh018-1V8': np.array([15.0, 15.0, 15.0, 15.0, 9.0, 9.0, 9.0, 9.0, 9.0, 15.0])
            , }.get(ace_backend, NotImplementedError(err))
    gm    = np.array([(i in range(0,4))  for i in range(10)])
    fm    = np.array([(i in range(4,8))  for i in range(10)])
    im    = np.array([(i in range(8,10)) for i in range(10)])
    return (x_min, x_max, gm, fm, im)

def reference_goal(constraints: dict, ace_backend: str) -> np.ndarray:
    """ Corated Referece Goal for OP2 """
    err   = f'No Reference Goal for {ace_backend} available'
    vdd   = constraints.get('vsup', {}).get('init', 3.3)
    return { 'xh035-3V3': { "A":           5.0e-10      # 5.010925e-10
                          , "a_0":         55.0         # 54.962221293150016
                          , "ugbw":        3.5e6        # 3428563.930768671
                          , "sr_r":        3.5e6        # 3822408.8725046776
                          , "sr_f":        3.5e6        # -3846399.224656781
                          , "pm":          65.0         # 67.0570640439259
                          , "gm":          -30.0        # -32.298672913767724
                          , "cmrr":        100.0        # 101.52646998121247
                          , "psrr_n":      55.0         # 55.22058921101098
                          , "psrr_p":      90.0         # 91.50247601455912
                          , "idd":         3.0e-5       # 3.0211906622006625e-05
                          , "iss":         3.3e-5       # -3.3211921814583654e-05
                          , "vn_1Hz":      6.5e-6       # 6.216847362829546e-06
                          , "vn_10Hz":     2.0e-6       # 1.8361486757073514e-06
                          , "vn_100Hz":    5.5e-7       # 5.395284017023125e-07
                          , "vn_1kHz":     1.75e-7      # 1.6163236371474532e-07
                          , "vn_10kHz":    6.5e-8       # 6.295679831589233e-08
                          , "vn_100kHz":   4.5e-8       # 4.421652882505914e-08
                          , "cof":         35.0e6       # 34532197.91934585
                          , "overshoot_r": 2.5          # 2.6405786027522846
                          , "overshoot_f": 2.0          # 2.152491375598402
                          , "i_out_min":   -2.5e-5      # -2.34598447270796e-05
                          , "i_out_max":   2.5e-5       # 2.375395528802124e-05
                          , "v_ol":        (vdd * 0.50) # 1.6314814360399006
                          , "v_oh":        (vdd * 0.95) # 1.6685034539424761
                          , "v_il":        (vdd * 0.25) # 0.5688672464434619
                          , "v_ih":        (vdd * 0.95) # 3.3502486012612174
                          , "voff_stat":   3.0e-3       # 0.0031193237064727104
                          , "voff_sys":    -1.5e-3      # -0.0015180853180561346
                          , }
           , 'xh018-1V8': { "A":           5.0e-10      # 5.010925e-10
                          , "a_0":         55.0         # 54.962221293150016
                          , "ugbw":        3.5e6        # 3428563.930768671
                          , "sr_r":        3.5e6        # 3822408.8725046776
                          , "sr_f":        3.5e6        # -3846399.224656781
                          , "pm":          65.0         # 67.0570640439259
                          , "gm":          -30.0        # -32.298672913767724
                          , "cmrr":        100.0        # 101.52646998121247
                          , "psrr_n":      55.0         # 55.22058921101098
                          , "psrr_p":      90.0         # 91.50247601455912
                          , "idd":         3.0e-5       # 3.0211906622006625e-05
                          , "iss":         3.3e-5       # -3.3211921814583654e-05
                          , "vn_1Hz":      6.5e-6       # 6.216847362829546e-06
                          , "vn_10Hz":     2.0e-6       # 1.8361486757073514e-06
                          , "vn_100Hz":    5.5e-7       # 5.395284017023125e-07
                          , "vn_1kHz":     1.75e-7      # 1.6163236371474532e-07
                          , "vn_10kHz":    6.5e-8       # 6.295679831589233e-08
                          , "vn_100kHz":   4.5e-8       # 4.421652882505914e-08
                          , "cof":         35.0e6       # 34532197.91934585
                          , "overshoot_r": 2.5          # 2.6405786027522846
                          , "overshoot_f": 2.0          # 2.152491375598402
                          , "i_out_min":   -2.5e-5      # -2.34598447270796e-05
                          , "i_out_max":   2.5e-5       # 2.375395528802124e-05
                          , "v_ol":        (vdd * 0.50) # 1.6314814360399006
                          , "v_oh":        (vdd * 0.95) # 1.6685034539424761
                          , "v_il":        (vdd * 0.25) # 0.5688672464434619
                          , "v_ih":        (vdd * 0.95) # 3.3502486012612174
                          , "voff_stat":   3.0e-3       # 0.0031193237064727104
                          , "voff_sys":    -1.5e-3      # -0.0015180853180561346
                          , }
           , }.get(ace_backend, NotImplementedError(err))

def output_scale( constraints: dict, ace_backend: str
                ) -> tuple[dict[str, float], dict[str,float]]:
    """ Extimated Min/Max values for scaling 'perf' """
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
