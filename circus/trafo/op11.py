""" Agnostic Design Space Transforation for OP11: Rail-to-Rail Folded-Cascode
with Wide-Swing Current Mirror """

from fractions import Fraction
from typing import Any, List, Optional, Type, Union, Callable
import numpy as np

from ..prim import PrimitiveDevice

INPUTS: [str] = [ 'MND11:gmoverid',  'MPD21:gmoverid',  'MNCM11:gmoverid'
                , 'MNLS11:gmoverid', 'MNR1:gmoverid',   'MPCM21:gmoverid'
                , 'MPR2:gmoverid',   'MPCM31:gmoverid', 'MNCM41:gmoverid'
                , 'MND11:fug',       'MPD21:fug',       'MNCM11:fug'
                , 'MNLS11:fug',      'MNR1:fug',        'MPCM21:fug'
                , 'MPR2:fug',        'MPCM31:fug',      'MNCM41:fug'
                , 'MNCM43:id',       'MNCM32:id',       'MNCM44:id'
                , 'MPCM33:id',       'MPCM34:id' ]

def transform( constraints: dict, nmos: PrimitiveDevice, pmos: PrimitiveDevice
             , gmid_dp1: float, gmid_dp2: float, gmid_cm1: float, gmid_ls1: float
             , gmid_rs1: float, gmid_cm2: float, gmid_rs2: float, gmid_cm3: float
             , gmid_cm4: float
             , fug_dp1: float, fug_dp2: float, fug_cm1: float, fug_ls1: float
             , fug_rs1: float, fug_cm2: float, fug_rs2: float, fug_cm3: float
             , fug_cm4: float
             , i1: float, i2: float, i3: float, i4: float, iX: float
             ) -> dict[str, float]:
    """ Transforation for OP11 """
    i0      = constraints.get("i0",   {}).get("init", 3e-6)
    vdd     = constraints.get("vsup", {}).get("init", 3.3)

    W1_lim  = constraints.get("Mcm1", {}).get("max", 42)
    W2_lim  = constraints.get("Mcm1", {}).get("max", 42)

    iU      = i0 / 2.0
    iV      = abs(i1 / 2.0) + iX
    iY      = abs(i2 / 2.0) + iX

    Mdp1    = constraints.get("Md1", {}).get("init", 2)
    Mdp2    = constraints.get("Md2", {}).get("init", 2)
    Mcm31   = 1
    Mcm32   = max(int(i2 / iU), 1) * Mcm31
    Mcm33   = max(int(i4 / iU), 1) * Mcm31
    Mcm34   = max(int(iV / iU), 1) * Mcm31
    Mcm41   = 2
    Mcm42   = int(Mcm41 / 2)
    Mcm43   = max(int(i1 / i0), 1) * Mcm41
    Mcm44   = max(int(i3 / i0), 1) * Mcm41

    dp1_in  = np.array([[gmid_dp1, fug_dp1,  (vdd / 1.65), -(vdd /  5.0)]])
    dp2_in  = np.array([[gmid_dp2, fug_dp2, -(vdd / 1.65),  (vdd /  5.0)]])
    cm1_in  = np.array([[gmid_cm1, fug_cm1,  (vdd / 16.6),          0.0 ]])
    ls1_in  = np.array([[gmid_ls1, fug_ls1,  (vdd / 6.0),  -(vdd / 16.5)]])
    rs1_in  = np.array([[gmid_rs1, fug_rs1,  (vdd / 3.5),           0.0 ]])
    cm2_in  = np.array([[gmid_cm2, fug_cm2, -(vdd / 1.65),  (vdd /  5.5)]])
    rs2_in  = np.array([[gmid_rs2, fug_rs2, -(vdd / 2.0),           0.0 ]])
    cm3_in  = np.array([[gmid_cm3, fug_cm3, -(vdd / 3.5),           0.0 ]])
    cm4_in  = np.array([[gmid_cm4, fug_cm4,  (vdd / 4.5),           0.0 ]])

    dp1_out = nmos.predict(dp1_in)[0]
    dp2_out = pmos.predict(dp2_in)[0]
    cm1_out = nmos.predict(cm1_in)[0]
    ls1_out = nmos.predict(ls1_in)[0]
    rs1_out = nmos.predict(rs1_in)[0]
    cm2_out = pmos.predict(cm2_in)[0]
    rs2_out = pmos.predict(rs2_in)[0]
    cm3_out = pmos.predict(cm3_in)[0]
    cm4_out = nmos.predict(cm4_in)[0]

    Ldp1    = dp1_out[1]
    Ldp2    = dp2_out[1]
    Lcm1    = cm1_out[1]
    Lls1    = ls1_out[1]
    Lrs1    = rs1_out[1]
    Lcm2    = cm2_out[1]
    Lrs2    = rs2_out[1]
    Lcm3    = cm3_out[1]
    Lcm4    = cm4_out[1]

    Wc1     = iY / cm1_out[0]
    Wl1     = iX  / ls1_out[0]
    Wc2     = iX  / cm2_out[0]

    Mcm1    = np.ceil(Wc1 / W1_lim).item()
    Mls1    = np.ceil(Wl1 / W1_lim).item()
    Mcm2    = np.ceil(Wc2 / W2_lim).item()

    Wdp1    = i1 / 2.0 / dp1_out[0] / Mdp1
    Wdp2    = i2 / 2.0 / dp2_out[0] / Mdp2
    Wcm1    = Wc1 / Mcm1
    Wls1    = Wl1 / Mls1
    Wrs1    = i4 / rs1_out[0]
    Wcm2    = Wc2 / Mcm2
    Wrs2    = i3 / rs2_out[0]
    Wcm3    = iU / cm3_out[0]
    Wcm4    = i0 / cm4_out[0]

    sizing  = { 'Ld1':  Ldp1, 'Ld2': Ldp2, 'Lcm1': Lcm1, 'Lls1':  Lls1, 'Lr1': Lrs1
              , 'Lcm2': Lcm2, 'Lr2': Lrs2, 'Lcm3': Lcm3, 'Lcm4': Lcm4
              , 'Wd1':  Wdp1, 'Wd2': Wdp2, 'Wcm1': Wcm1, 'Wls1':  Wls1, 'Wr1': Wrs1
              , 'Wcm2': Wcm2, 'Wr2': Wrs2, 'Wcm3': Wcm3, 'Wcm4': Wcm4
              , 'Md1':  Mdp1, 'Md2': Mdp2, 'Mcm1': Mcm1, 'Mls1': Mls1, 'Mcm2': Mcm2
              , 'Mcm31': Mcm31, 'Mcm32': Mcm32, 'Mcm33': Mcm33, 'Mcm34': Mcm34
              , 'Mcm41': Mcm41, 'Mcm42': Mcm42, 'Mcm43': Mcm43, 'Mcm44': Mcm44
              , }

    return sizing

def unscaler(ace_backend: str) -> tuple[ np.ndarray, np.ndarray, np.ndarray
                                       , np.ndarray, np.ndarray]:
    """ Unscale function for a given PDK """
    err   = f'No Input Scale for {ace_backend} available'
    x_min = { 'xh035-3V3': np.array([ 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0
                                    , 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0
                                    , 3.0, 3.0, 3.0, 1.0, 3.0 ])
            , 'xh018-1V8': np.array([ 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0
                                    , 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0
                                    , 3.0, 3.0, 3.0, 1.0, 3.0 ])
            , }.get(ace_backend, NotImplementedError(err))
    x_max = { 'xh035-3V3': np.array([ 15.0, 15.0, 15.0, 15.0, 15.0, 15.0, 15.0, 15.0, 15.0
                                    , 9.0, 9.0, 9.0, 9.0, 9.0, 9.0, 9.0, 9.0, 9.0
                                    , 9.0, 9.0, 9.0, 2.0, 9.0 ])
            , 'xh018-1V8': np.array([ 15.0, 15.0, 15.0, 15.0, 15.0, 15.0, 15.0, 15.0, 15.0
                                    , 9.0, 9.0, 9.0, 9.0, 9.0, 9.0, 9.0, 9.0, 9.0
                                    , 9.0, 9.0, 9.0, 2.0, 9.0 ])
            , }.get(ace_backend, NotImplementedError(err))
    gm    = np.array([(i in range(0,9))   for i in range(23)])
    fm    = np.array([(i in range(9,18))  for i in range(23)])
    im    = np.array([(i in range(18,23)) for i in range(23)])
    return (x_min, x_max, gm, fm, im)

def reference_goal(constraints: dict, ace_backend: str) -> np.ndarray:
    """ Corated Referece Goal for OP8 """
    err   = f'No Reference Goal for {ace_backend} available'
    vdd   = constraints.get('vsup', {}).get('init', 3.3)
    return { 'xh035-3V3': { "A":                    0.00015
                          , "a_0":                  65
                          , "ugbw":                 5000000.0
                          , "sr_r":                 2500000.0
                          , "sr_f":                 2500000.0
                          , "pm":                   45.0
                          , "gm":                   -50.0
                          , "cmrr":                 120.0
                          , "psrr_n":               80.0
                          , "psrr_p":               100.0
                          , "idd":                  1.0e-4
                          , "iss":                  -0.0001
                          , "vn_1Hz":               3.5e-06
                          , "vn_10Hz":              1.0e-06
                          , "vn_100Hz":             5.0e-07
                          , "vn_1kHz":              1.65e-07
                          , "vn_10kHz":             5.0e-08
                          , "vn_100kHz":            2.5e-08
                          , "cof":                  150000000.0
                          , "overshoot_r":          8000000.0
                          , "overshoot_f":          250000000.0
                          , "i_out_min":            -2.0e-05
                          , "i_out_max":            3.5e-05
                          , "v_ol":                 (vdd * 0.45)
                          , "v_oh":                 (vdd * 0.55)
                          , "v_il":                 (vdd * 0.1)
                          , "v_ih":                 (vdd * 1.0)
                          , "voff_stat":            1.5e-3
                          , "voff_sys":             0.05 }
           , 'xh018-1V8': { "A":                    0.00015
                          , "a_0":                  65
                          , "ugbw":                 5000000.0
                          , "sr_r":                 2500000.0
                          , "sr_f":                 2500000.0
                          , "pm":                   45.0
                          , "gm":                   -50.0
                          , "cmrr":                 120.0
                          , "psrr_n":               80.0
                          , "psrr_p":               100.0
                          , "idd":                  1.0e-4
                          , "iss":                  -0.0001
                          , "vn_1Hz":               3.5e-06
                          , "vn_10Hz":              1.0e-06
                          , "vn_100Hz":             5.0e-07
                          , "vn_1kHz":              1.65e-07
                          , "vn_10kHz":             5.0e-08
                          , "vn_100kHz":            2.5e-08
                          , "cof":                  150000000.0
                          , "overshoot_r":          8000000.0
                          , "overshoot_f":          250000000.0
                          , "i_out_min":            -2.0e-05
                          , "i_out_max":            3.5e-05
                          , "v_ol":                 (vdd * 0.45)
                          , "v_oh":                 (vdd * 0.55)
                          , "v_il":                 (vdd * 0.1)
                          , "v_ih":                 (vdd * 1.0)
                          , "voff_stat":            1.5e-3
                          , "voff_sys":             0.05 }
           , }.get(ace_backend, NotImplementedError(err))

def output_scale( constraints: dict, ace_backend: str
                ) -> tuple[dict[str, float], dict[str, float]]:
    err   = f'No Performance Scale for {ace_backend} available'
    vdd   = constraints.get('vsup', {}).get('init', 3.3)

    x_min = { 'xh035-3V3': { "a_0":         -120.0
                           , "ugbw":        0.0
                           , "pm":          0.0
                           , "gm":          0.0
                           , "cmrr":        10.0
                           , "sr_r":        0.0
                           , "sr_f":        0.0
                           , "vn_1Hz":      -10.0
                           , "vn_10Hz":     -10.0
                           , "vn_100Hz":    -10.0
                           , "vn_1kHz":     -10.0
                           , "vn_10kHz":    -10.0
                           , "vn_100kHz":   -10.0
                           , "psrr_n":      2.0
                           , "psrr_p":      40.0
                           , "v_il":        0.0
                           , "v_ih":        0.0
                           , "v_ol":        0.0
                           , "v_oh":        1.0
                           , "i_out_min":   -4.0
                           , "i_out_max":   -7.0
                           , "idd":         -5.0
                           , "iss":         -4.0
                           , "overshoot_r": 0.0
                           , "overshoot_f": 0.0
                           , "cof":         0.0
                           , "voff_stat":   -5.0
                           , "voff_sys":    -0.2
                           , "A":           -5.0 }
            , 'xh018-1V8': { "a_0":         -120.0
                           , "ugbw":        0.0
                           , "pm":          0.0
                           , "gm":          0.0
                           , "cmrr":        10.0
                           , "sr_r":        0.0
                           , "sr_f":        0.0
                           , "vn_1Hz":      -10.0
                           , "vn_10Hz":     -10.0
                           , "vn_100Hz":    -10.0
                           , "vn_1kHz":     -10.0
                           , "vn_10kHz":    -10.0
                           , "vn_100kHz":   -10.0
                           , "psrr_n":      2.0
                           , "psrr_p":      40.0
                           , "v_il":        0.0
                           , "v_ih":        0.0
                           , "v_ol":        0.0
                           , "v_oh":        1.0
                           , "i_out_min":   -4.0
                           , "i_out_max":   -7.0
                           , "idd":         -5.0
                           , "iss":         -4.0
                           , "overshoot_r": 0.0
                           , "overshoot_f": 0.0
                           , "cof":         0.0
                           , "voff_stat":   -5.0
                           , "voff_sys":    -0.2
                           , "A":           -5.0 }
            , }.get(ace_backend, NotImplementedError(err))
    x_max = { 'xh035-3V3': { "a_0":         100.0
                           , "ugbw":        15000000.0
                           , "pm":          175.0
                           , "gm":          25.0
                           , "cmrr":        200.0
                           , "sr_r":        15000000.0
                           , "sr_f":        15000000.0
                           , "vn_1Hz":      -4.0
                           , "vn_10Hz":     -4.0
                           , "vn_100Hz":    -4.0
                           , "vn_1kHz":     -4.0
                           , "vn_10kHz":    -4.0
                           , "vn_100kHz":   -4.0
                           , "psrr_n":      150.0
                           , "psrr_p":      200.0
                           , "v_il":        vdd
                           , "v_ih":        2 * vdd
                           , "v_ol":        vdd
                           , "v_oh":        vdd
                           , "i_out_min":   -7.0
                           , "i_out_max":   0.00017612534902145907
                           , "idd":         0.0003738925335125203
                           , "iss":         -5.0
                           , "overshoot_r": 40000000000.0
                           , "overshoot_f": 300000000000.0
                           , "cof":         100000000000.0
                           , "voff_stat":   0.75
                           , "voff_sys":    1.65
                           , "A":           -3.5 }
            , 'xh018-1V8': { "a_0":         100.0
                           , "ugbw":        15000000.0
                           , "pm":          175.0
                           , "gm":          25.0
                           , "cmrr":        200.0
                           , "sr_r":        15000000.0
                           , "sr_f":        15000000.0
                           , "vn_1Hz":      -4.0
                           , "vn_10Hz":     -4.0
                           , "vn_100Hz":    -4.0
                           , "vn_1kHz":     -4.0
                           , "vn_10kHz":    -4.0
                           , "vn_100kHz":   -4.0
                           , "psrr_n":      150.0
                           , "psrr_p":      200.0
                           , "v_il":        vdd
                           , "v_ih":        2 * vdd
                           , "v_ol":        vdd
                           , "v_oh":        vdd
                           , "i_out_min":   -7.0
                           , "i_out_max":   0.00017612534902145907
                           , "idd":         0.0003738925335125203
                           , "iss":         -5.0
                           , "overshoot_r": 40000000000.0
                           , "overshoot_f": 300000000000.0
                           , "cof":         100000000000.0
                           , "voff_stat":   0.75
                           , "voff_sys":    1.65
                           , "A":           -3.5 }
            , }.get(ace_backend, NotImplementedError(err))
    return (x_min, x_max)
