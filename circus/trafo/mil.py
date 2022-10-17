"""
Agnostic Design Space Transforation for MIL: Miller Operational Amplifier

`INPUTS` are:

    [ 'MNCM11_gmoverid', 'MPCM21_gmoverid', 'MPCS11_gmoverid', 'MNDP11_gmoverid'
    , 'MNCM11_fug',      'MPCM21_fug',      'MPCS11_fug',      'MNDP11_fug'
    , 'MNCM12_id',       'MNCM13_id' ]
"""

# from fractions import Fraction
# from typing import Callable
import numpy as np
import torch as pt
import pandas as pd

INPUTS: [str] = [ 'MNCM11_gmoverid', 'MPCM21_gmoverid', 'MPCS11_gmoverid', 'MNDP11_gmoverid'
                , 'MNCM11_fug',      'MPCM21_fug',      'MPCS11_fug',      'MNDP11_fug'
                , 'MNCM12_id',       'MNCM13_id' ]

def transform( constraints: dict, nmos: pt.nn.Module, pmos: pt.nn.Module
             # , res: Callable, cap: Callable
             , gmid_cm1: float, gmid_cm2: float, gmid_cs1: float, gmid_dp1: float
             , fug_cm1: float,  fug_cm2: float,  fug_cs1: float,  fug_dp1: float
             #, rc: float, cc: float
             , i1: float, i2: float
             ) -> dict[str, float]:
    """ Electrical to Geometrical Transforation for MIL """

    i0      = constraints.get('i0',  3e-6)
    vdd     = constraints.get('vdd', 1.8)

    Wres    = constraints.get('Wres', 2e-6)
    Lres    = constraints.get('Lres', 113e-6)
    Wcap    = constraints.get('Wcap', 69e-6)
    Mcap    = constraints.get('Mcap', 1)

    Mcm21   = constraints.get('Mcm21', 2)
    Mcm22   = constraints.get('Mcm22', 2)
    Mdp11   = constraints.get('Mdp11', 2)

    M1_lim  = 40
    M2_lim  = 40

    Mcm11   = 1
    Mcm12   = max(min(round(i1 / i0), M1_lim), 1)
    Mcm13   = max(min(round(i2 / i0), M1_lim), 1)
    Mcs11    = Mcm13

    cm1_in  = pt.Tensor([[gmid_cm1, fug_cm1,  (vdd / 4.20),         0.00 ]])
    cm2_in  = pt.Tensor([[gmid_cm2, fug_cm2, -(vdd / 3.55),         0.00 ]])
    cs1_in  = pt.Tensor([[gmid_cs1, fug_cs1, -(vdd / 2.00),         0.00 ]])
    dp1_in  = pt.Tensor([[gmid_dp1, fug_dp1,  (vdd / 2.24), -(vdd / 4.25)]])

    cm1_out = nmos(cm1_in).numpy()[0]
    cm2_out = pmos(cm2_in).numpy()[0]
    cs1_out = pmos(cs1_in).numpy()[0]
    dp1_out = nmos(dp1_in).numpy()[0]

    Lcm1    = cm1_out[1]
    Lcm2    = cm2_out[1]
    Lcs1    = cs1_out[1]
    Ldp1    = dp1_out[1]

    Wcm1    = i0       / cm1_out[0] / Mcm11
    Wcm2    = i1 / 2.0 / cm2_out[0] / Mcm21
    Wdp1    = i1 / 2.0 / dp1_out[0] / Mdp11
    Wcs     = i2       / cs1_out[0]
    Wcs1    = Wcs                   / Mcs11

    keys    = [ 'Ldp1'  , 'Lcm1',  'Lcm2',  'Lcs1', 'Lres'
              , 'Wdp1'  , 'Wcm1',  'Wcm2',  'Wcs1', 'Wres', 'Wcap'
              , 'Mdp11' , 'Mcm11', 'Mcm21', 'Mcs11',        'Mcap'
                        , 'Mcm12', 'Mcm22'
                        , 'Mcm13' ]

    values  = [ Ldp1,  Lcm1,  Lcm2,  Lcs1,  Lres
              , Wdp1,  Wcm1,  Wcm2,  Wcs1,  Wres, Wcap
              , Mdp11, Mcm11, Mcm21, Mcs11,       Mcap
                            , Mcm12, Mcm22
                            , Mcm13 ]

    sizing  = pd.DataFrame(np.array([values]), columns = keys)

    return sizing

def unscaler() -> tuple[ np.ndarray, np.ndarray, np.ndarray
                       , np.ndarray, np.ndarray ]:
    """ Upper and lower bounds and selection masks """
    x_min = np.array([ 5.0, 10.0, 5.0, 10.0
                     , 7.0, 7.0, 7.0, 7.0
                     , 3.0, 45.0 ])
    x_max = np.array([ 15.0, 20.0, 15.0, 20.0
                     , 9.0, 9.0, 9.0, 9.0
                     , 9.0, 75.0 ])
    gm    = np.array([(i in range(0,4))  for i in range(10)])
    fm    = np.array([(i in range(4,8))  for i in range(10)])
    im    = np.array([(i in range(8,10)) for i in range(10)])
    return (x_min, x_max, gm, fm, im)

def reference_goal(constraints: dict) -> dict[str,float]:
    """ Curated Referece Goal for MIL """
    vdd = constraints.get('vdd', 1.8)
    return { "area":        5.5e-9         # 5.38162e-09
           , "a_0":         100.0          # 104.83873351808626
           , "ugbw":        1.0e6          # 1007672.6892557623
           , "sr_r":        1.0e6          # 643626.640626512
           , "sr_f":        -1.0e6         # -635172.5669242825
           , "pm":          90.0           # 92.46348312601351
           , "gm":          -90.0          # -94.0228120184453
           , "cmrr":        120.0          # 121.41787866754784
           , "psrr_n":      100.0          # 108.88639881084693
           , "psrr_p":      100.0          # 109.58280488887551
           , "idd":         7.0e-5         # 6.945603045871478e-05
           , "iss":         -7.5e-5        # -7.245603283577388e-05
           , "vn_1Hz":      5.0e-6         # 5.083454785444561e-06
           , "vn_10Hz":     1.5e-6         # 1.4998955809756694e-06
           , "vn_100Hz":    4.5e-7         # 4.4048325646935895e-07
           , "vn_1kHz":     1.5e-5         # 1.3244013240248254e-07
           , "vn_10kHz":    5.5e-8         # 5.297534060968821e-08
           , "vn_100kHz":   4.0e-8         # 3.831101172886542e-08
           , "cof":         2.0e9          # 2127642604.233062
           , "os_r":        0.5e-3         # 0.0005518141734703779
           , "os_f":        0.5e-3         # 0.00047131508580914634
           , "i_out_min":   -5.0e-3        # -0.003998561000759212
           , "i_out_max":   7.0e-5         # 6.795110367221515e-05
           , "v_ol":        (vdd * 0.0333) # 0.1189121584287387
           , "v_oh":        (vdd * 0.82)   # 3.142843762405591
           , "v_il":        (vdd * 0.25)   # 0.7159757161850907
           , "v_ih":        (vdd * 0.82)   # 3.140097305913386
           , "voff_stat":   3.0e-3         # 0.002987252118372549
           , "voff_syst":   -250.0e-6      # -0.0002386325463920591
           , }

def output_scale( constraints: dict
                ) -> tuple[dict[str, float], dict[str, float]]:
    """
    Estimated [-1.0;1.0] scaler for the Performance obtained from serafin.
    Arguments:
        - `constraints`: Design constraints obtained from serafin.
    """
    vdd   = constraints.get('vdd', 1.8)
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
            , 'os_r'        : 0.0
            , 'os_f'        : 0.0
            , 'cof'         : 5.0
            , 'voff_stat'   : -5.0
            , 'voff_syst'   : -5.0
            , 'area'        : -15.0
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
            , 'os_r'        : 130.0
            , 'os_f'        : 130.0
            , 'cof'         : 9.0
            , 'voff_stat'   : 0.0
            , 'voff_syst'   : 0.0
            , 'area'        : -5.0
            , }
    return (x_min, x_max)
