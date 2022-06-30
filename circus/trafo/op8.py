""" Agnostic Design Space Transforation for OP8: Folded Cascode """

from fractions import Fraction
from typing import Any, List, Optional, Type, Union, Callable
import numpy as np

from ..prim import PrimitiveDevice

INPUTS: [str] = [ 'MNCM51:gmoverid', 'MPCM41:gmoverid', 'MPCM31:gmoverid'
                , 'MNCM21:gmoverid', 'MNCM11:gmoverid', 'MND11:gmoverid'
                , 'MNCM51:fug',      'MPCM41:fug',      'MPCM31:fug'
                , 'MNCM21:fug',      'MNCM11:fug',      'MND11:fug'
                , 'MNCM53:id',       'MNCM21:id' ]

def transform( constraints: dict, nmos: PrimitiveDevice, pmos: PrimitiveDevice
             , gmid_cm1: float, gmid_cm2: float, gmid_cm3: float
             , gmid_cm4: float, gmid_cm5: float, gmid_dp1: float
             , fug_cm1: float,  fug_cm2: float,  fug_cm3: float
             , fug_cm4: float,  fug_cm5: float,  fug_dp1: float
             , i1: float, i4: float ) -> dict[str, float]:
    """ Transforation for OP8 """

    i2      = i1
    i3      = (i1 / 2.0) + i4

    i0      = constraints.get("i0",   {}).get("init", 3e-6)
    vdd     = constraints.get("vsup", {}).get("init", 3.3)

    M5_lim  = int(constraints.get("Mcm53", {}).get("max", 42))
    M4_lim  = int(constraints.get("Mcm43", {}).get("max", 42))

    W1_lim  = float(constraints.get("Wcm1", {}).get("max", 100e-6))
    W2_lim  = float(constraints.get("Wcm2", {}).get("max", 100e-6))
    W3_lim  = float(constraints.get("Wcm3", {}).get("max", 100e-6))

    M5      = Fraction(i0 / i1).limit_denominator(M5_lim)
    M4      = Fraction(i2 / i3).limit_denominator(M4_lim)

    Mdp1    = constraints.get("Md1", {}).get("init", 2)

    Mcm51   = max(M5.numerator, 1)
    Mcm52   = Mcm53 = max(M5.denominator, 1)
    Mcm41   = max(M4.numerator, 1)
    Mcm42   = Mcm43 = max(M4.denominator, 1)

    cm1_in  = np.array([[gmid_cm1, fug_cm1,  (vdd / 5.0),         0.0 ]])
    cm2_in  = np.array([[gmid_cm2, fug_cm2,  (vdd / 3.5), -(vdd / 5.0)]])
    cm3_in  = np.array([[gmid_cm3, fug_cm3, -(vdd / 3.0),  (vdd / 5.0)]])
    cm4_in  = np.array([[gmid_cm4, fug_cm4, -(vdd / 3.5),         0.0 ]])
    cm5_in  = np.array([[gmid_cm5, fug_cm5,  (vdd / 4.5),         0.0 ]])
    dp1_in  = np.array([[gmid_dp1, fug_dp1,  (vdd / 2.0), -(vdd / 4.5)]])

    cm1_out = nmos.predict(cm1_in)[0]
    cm2_out = nmos.predict(cm2_in)[0]
    cm3_out = pmos.predict(cm3_in)[0]
    cm4_out = pmos.predict(cm4_in)[0]
    cm5_out = nmos.predict(cm5_in)[0]
    dp1_out = nmos.predict(dp1_in)[0]

    Lcm1    = cm1_out[1]
    Lcm2    = cm2_out[1]
    Lcm3    = cm3_out[1]
    Lcm4    = cm4_out[1]
    Lcm5    = cm5_out[1]
    Ldp1    = dp1_out[1]

    Wc1     = i4 / cm1_out[0]
    Wc2     = i4 / cm1_out[0]
    Wc3     = i4 / cm1_out[0]

    Mcm1    = np.ceil(Wc1 / W1_lim).item()
    Mcm2    = np.ceil(Wc1 / W2_lim).item()
    Mcm3    = np.ceil(Wc1 / W3_lim).item()
    Wcm1    = Wc1 / Mcm1
    Wcm2    = Wc2 / Mcm2
    Wcm3    = Wc3 / Mcm3

    Wcm4    = i2       / cm4_out[0] / Mcm41
    Wcm5    = i0       / cm5_out[0] / Mcm51
    Wdp1    = i1 / 2.0 / dp1_out[0] / Mdp1

    sizing  = { 'Ld1': Ldp1, 'Lcm1': Lcm1, 'Lcm2': Lcm2, 'Lcm3': Lcm3, 'Lcm4':  Lcm4,  'Lcm5':  Lcm5
              , 'Wd1': Wdp1, 'Wcm1': Wcm1, 'Wcm2': Wcm2, 'Wcm3': Wcm3, 'Wcm4':  Wcm4,  'Wcm5':  Wcm5
              , 'Md1': Mdp1, 'Mcm1': Mcm1, 'Mcm2': Mcm2, 'Mcm3': Mcm3, 'Mcm41': Mcm41, 'Mcm51': Mcm51
                                                                     , 'Mcm42': Mcm42, 'Mcm52': Mcm52
                                                                     , 'Mcm43': Mcm43, 'Mcm53': Mcm53
              , }

    return sizing

def unscaler(ace_backend: str) -> tuple[ np.ndarray, np.ndarray, np.ndarray
                                       , np.ndarray, np.ndarray]:
    """ Unscale function for a given PDK """
    err   = f'No Input Scale for {ace_backend} available'
    x_min = { 'xh035-3V3': np.array([ 5.0, 5.0, 5.0, 5.0, 5.0, 5.0
                                    , 7.0, 7.0, 7.0, 7.0, 7.0, 7.0
                                    , 1.0, 3.0 ])
            , 'xh018-1V8': np.array([ 5.0, 5.0, 5.0, 5.0, 5.0, 5.0
                                    , 7.0, 7.0, 7.0, 7.0, 7.0, 7.0
                                    , 1.0, 3.0 ])
            , }.get(ace_backend, NotImplementedError(err))
    x_max = { 'xh035-3V3': np.array([ 15.0, 15.0, 15.0, 15.0, 15.0, 15.0
                                    , 9.0, 9.0, 9.0, 9.0, 9.0, 9.0
                                    , 6.0, 9.0 ])
            , 'xh018-1V8': np.array([ 15.0, 15.0, 15.0, 15.0, 15.0, 15.0
                                    , 9.0, 9.0, 9.0, 9.0, 9.0, 9.0
                                    , 6.0, 9.0 ])
            , }.get(ace_backend, NotImplementedError(err))
    gm    = np.array([(i in range(0,6))   for i in range(14)])
    fm    = np.array([(i in range(6,12))  for i in range(14)])
    im    = np.array([(i in range(12,14)) for i in range(14)])
    return (x_min, x_max, gm, fm, im)

def reference_goal(constraints: dict, ace_backend: str) -> np.ndarray:
    """ Corated Referece Goal for OP8 """
    err   = f'No Reference Goal for {ace_backend} available'
    vdd   = constraints.get('vsup', {}).get('init', 3.3)
    return { 'xh035-3V3': { "A":           5.5e-10      # 8.35135e-10
                          , "a_0":         65.0         # 65.50825257646494
                          , "ugbw":        750.0e3      # 608137.1389850643
                          , "sr_r":        750.0e3      # 482568.7087129002
                          , "sr_f":        750.0e3      # -478544.5088903557
                          , "pm":          80.0         # 89.13695404645551
                          , "gm":          -65.0        # -67.66169835915815
                          , "cmrr":        120.0        # 162.47373336546218
                          , "psrr_n":      100.0        # 100.13765587162408
                          , "psrr_p":      120.0        # 129.22912741937355
                          , "idd":         1.75e-5      # 1.5197106684950545e-05
                          , "iss":         -2.0e-5      # -1.8197106699045546e-05
                          , "vn_1Hz":      1.5e-5       # 1.6051837422213292e-05
                          , "vn_10Hz":     4.5e-6       # 4.7505758803117315e-06
                          , "vn_100Hz":    1.5e-6       # 1.397702658168099e-06
                          , "vn_1kHz":     4.0e-7       # 4.1657014801681973e-07
                          , "vn_10kHz":    1.5e-7       # 1.5526276209235358e-07
                          , "vn_100kHz":   1.0e-7       # 1.0126074486509364e-07
                          , "cof":         300.0e6      # 281341676.572598
                          , "overshoot_r": 250.0e-6     # 0.0002498645125906737
                          , "overshoot_f": 250.0e-6     # 0.0002738703385872967
                          , "i_out_min":   -6.0e-6      # -6.031772879587186e-06
                          , "i_out_max":   8.5e-6       # 8.675972745540758e-06
                          , "v_ol":        (vdd * 0.45) # 1.5877847742499538
                          , "v_oh":        (vdd * 0.50) # 1.7122234338584263
                          , "v_il":        (vdd * 0.22) # 0.7476786622011943
                          , "v_ih":        (vdd * 1.00) # 3.7814460160662557
                          , "voff_stat":   5.0e-3       # 0.0072408778584526915
                          , "voff_sys":    -5.0e-7      # -4.817662030216676e-07
                          , }
           , 'xh018-1V8': { "A":           5.5e-10      # 8.35135e-10
                          , "a_0":         65.0         # 65.50825257646494
                          , "ugbw":        750.0e3      # 608137.1389850643
                          , "sr_r":        750.0e3      # 482568.7087129002
                          , "sr_f":        750.0e3      # -478544.5088903557
                          , "pm":          80.0         # 89.13695404645551
                          , "gm":          -65.0        # -67.66169835915815
                          , "cmrr":        120.0        # 162.47373336546218
                          , "psrr_n":      100.0        # 100.13765587162408
                          , "psrr_p":      120.0        # 129.22912741937355
                          , "idd":         1.75e-5      # 1.5197106684950545e-05
                          , "iss":         -2.0e-5      # -1.8197106699045546e-05
                          , "vn_1Hz":      1.5e-5       # 1.6051837422213292e-05
                          , "vn_10Hz":     4.5e-6       # 4.7505758803117315e-06
                          , "vn_100Hz":    1.5e-6       # 1.397702658168099e-06
                          , "vn_1kHz":     4.0e-7       # 4.1657014801681973e-07
                          , "vn_10kHz":    1.5e-7       # 1.5526276209235358e-07
                          , "vn_100kHz":   1.0e-7       # 1.0126074486509364e-07
                          , "cof":         300.0e6      # 281341676.572598
                          , "overshoot_r": 250.0e-6     # 0.0002498645125906737
                          , "overshoot_f": 250.0e-6     # 0.0002738703385872967
                          , "i_out_min":   -6.0e-6      # -6.031772879587186e-06
                          , "i_out_max":   8.5e-6       # 8.675972745540758e-06
                          , "v_ol":        (vdd * 0.45) # 1.5877847742499538
                          , "v_oh":        (vdd * 0.50) # 1.7122234338584263
                          , "v_il":        (vdd * 0.22) # 0.7476786622011943
                          , "v_ih":        (vdd * 1.00) # 3.7814460160662557
                          , "voff_stat":   5.0e-3       # 0.0072408778584526915
                          , "voff_sys":    -5.0e-7      # -4.817662030216676e-07
                          , }
           , }.get(ace_backend, NotImplementedError(err))

def output_scale( constraints: dict, ace_backend: str
                ) -> tuple[dict[str, float], dict[str, float]]:
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
