"""
Agnostic Design Space Transforation for RFA: Rail-to-Rail Folded-Cascode
with Wide-Swing Current Mirror

`INPUTS` are:

    [ 'MNDP11_gmoverid', 'MPDP21_gmoverid', 'MNCM11_gmoverid', 'MPCM21_gmoverid'
    , 'MNCM31_gmoverid', 'MNLS11_gmoverid', 'MPLS21_gmoverid', 'MNRF11_gmoverid'
    , 'MPRF21_gmoverid'
    , 'MNDP11_fug',      'MPDP21_fug',      'MNCM11_fug',      'MPCM21_fug'
    , 'MNCM31_fug',      'MNLS11_fug',      'MPLS21_fug',      'MNRF11_fug'
    , 'MPRF21_fug'
    , 'MNCM13_id', 'MNCM22_id', 'MNCM14_id' , 'MPCM24_id', 'MNLS11_id' ]

"""

# from fractions import Fraction
import numpy as np
import torch as pt
import pandas as pd

INPUTS: [str] = [ 'MNDP11_gmoverid', 'MPDP21_gmoverid', 'MNCM11_gmoverid', 'MPCM21_gmoverid'
                , 'MNCM31_gmoverid', 'MNLS11_gmoverid', 'MPLS21_gmoverid', 'MNRF11_gmoverid'
                , 'MPRF21_gmoverid'
                , 'MNDP11_fug',      'MPDP21_fug',      'MNCM11_fug',      'MPCM21_fug'
                , 'MNCM31_fug',      'MNLS11_fug',      'MPLS21_fug',      'MNRF11_fug'
                , 'MPRF21_fug'
                , 'MNCM13_id', 'MNCM22_id', 'MNCM14_id' , 'MPCM24_id', 'MNLS11_id' ]

def transform( constraints: dict, nmos: pt.nn.Module, pmos: pt.nn.Module
             , gmid_dp1: float, gmid_dp2: float, gmid_cm1: float, gmid_cm2: float
             , gmid_cm3: float, gmid_ls1: float, gmid_ls2: float, gmid_rf1: float
             , gmid_rf2: float
             , fug_dp1: float, fug_dp2: float, fug_cm1: float, fug_cm2: float
             , fug_cm3: float, fug_ls1: float, fug_ls2: float, fug_rf1: float
             , fug_rf2: float
             , i1: float, i2: float, i3: float, i4: float, iX: float
             ) -> pd.DataFrame:
    """ Electrical to Geometrical Transforation for RFA """
    i0      = constraints.get('i0',  3e-6)
    vdd     = constraints.get('vdd', 1.8)

    WS_lim  = constraints.get('Mls11', 42)
    WM_lim  = constraints.get('Mcm31', 42)

    w_max   = constraints.get('width', {}).get('max', 100e-6)

    iU      =     i0 / 2.0
    iV      = abs(i1 / 2.0) + iX
    iY      = abs(i2 / 2.0) + iX

    Mdp11   = constraints.get('Mdp11',  2)
    Mdp12   = constraints.get('Mdp12',  Mdp11)

    Mdp21   = constraints.get('Mdp21',  2)
    Mdp22   = constraints.get('Mdp12',  Mdp21)

    Mcm21   = constraints.get('Mcm21', 1)
    Mcm22   = max(int(i2 / iU), 1) * Mcm21
    Mcm23   = max(int(i4 / iU), 1) * Mcm21
    Mcm24   = Mcm25 = max(int(iV / iU), 1) * Mcm21

    Mcm11   = constraints.get('Mcm11', 2)
    Mcm12   = int(Mcm11 / 2)
    Mcm13   = max(int(i1 / i0), 1) * Mcm21
    Mcm14   = max(int(i3 / i0), 1) * Mcm21

    dp1_in  = pt.Tensor([[gmid_dp1, fug_dp1,  (vdd / 1.65), -(vdd /  5.0)]])
    dp2_in  = pt.Tensor([[gmid_dp2, fug_dp2, -(vdd / 1.65),  (vdd /  5.0)]])
    cm1_in  = pt.Tensor([[gmid_cm1, fug_cm1,  (vdd / 16.6),          0.0 ]])
    cm2_in  = pt.Tensor([[gmid_cm2, fug_cm2, -(vdd / 1.65),  (vdd /  5.5)]])
    cm3_in  = pt.Tensor([[gmid_cm3, fug_cm3, -(vdd / 3.5),           0.0 ]])
    ls1_in  = pt.Tensor([[gmid_ls1, fug_ls1,  (vdd / 6.0),  -(vdd / 16.5)]])
    ls2_in  = pt.Tensor([[gmid_ls2, fug_ls2,  (vdd / 4.5),           0.0 ]])
    rf1_in  = pt.Tensor([[gmid_rf1, fug_rf1,  (vdd / 3.5),           0.0 ]])
    rf2_in  = pt.Tensor([[gmid_rf2, fug_rf2, -(vdd / 2.0),           0.0 ]])

    dp1_out = nmos(dp1_in).numpy()[0]
    dp2_out = pmos(dp2_in).numpy()[0]
    cm1_out = nmos(cm1_in).numpy()[0]
    cm2_out = pmos(cm2_in).numpy()[0]
    cm3_out = nmos(cm3_in).numpy()[0]
    ls1_out = nmos(ls1_in).numpy()[0]
    ls2_out = pmos(ls2_in).numpy()[0]
    rf1_out = nmos(rf1_in).numpy()[0]
    rf2_out = pmos(rf2_in).numpy()[0]

    Ldp1    = dp1_out[1]
    Ldp2    = dp2_out[1]
    Lcm1    = cm1_out[1]
    Lcm2    = cm2_out[1]
    Lcm3    = cm3_out[1]
    Lls1    = ls1_out[1]
    Lls2    = ls2_out[1]
    Lrf1    = rf1_out[1]
    Lrf2    = rf2_out[1]

    Wc3     = iY / cm3_out[0]
    Wl1     = iX / ls1_out[0]
    Wl2     = iX / ls2_out[0]

    Mcm31   = Mcm32 = np.ceil(Wc3 / WM_lim).item()
    Mls11   = Mls12 = np.ceil(Wl1 / WS_lim).item()
    Mls21   = Mls22 = np.ceil(Wl2 / WS_lim).item()

    Wr1     = i4 / rf1_out[0]
    Wr2     = i3 / rf2_out[0]

    Mrf11   = int(max(Wr1 / w_max, constraints.get('Mrf11', 1)))
    Mrf21   = int(max(Wr2 / w_max, constraints.get('Mrf21', 1)))
    Wrf1    = Wr1 / Mrf11
    Wrf2    = Wr2 / Mrf21

    Wdp1    = i1 / 2.0 / dp1_out[0] / Mdp11
    Wdp2    = i2 / 2.0 / dp2_out[0] / Mdp21
    Wcm3    = Wc3 / Mcm31
    Wls1    = Wl1 / Mls11
    Wls2    = Wl2 / Mls21
    Wcm2    = iU / cm2_out[0]
    Wcm1    = i0 / cm1_out[0]

    keys    = [ 'Ldp1',  'Ldp2',  'Lcm1',  'Lcm2', 'Lcm3'
              , 'Lls1',  'Lls2',  'Lrf1',  'Lrf2'
              , 'Wdp1',  'Wdp2',  'Wcm1',  'Wcm2', 'Wcm3'
              , 'Wls1',  'Wls2',  'Wrf1',  'Wrf2'
              , 'Mdp11', 'Mdp21', 'Mcm11', 'Mcm21', 'Mcm31', 'Mls11', 'Mls21', 'Mrf11', 'Mrf21'
              , 'Mdp12', 'Mdp22', 'Mcm12', 'Mcm22', 'Mcm32', 'Mls12', 'Mls22'
                                , 'Mcm13', 'Mcm23'
                                , 'Mcm14', 'Mcm24'
                                         , 'Mcm25' ]

    values  = [ Ldp1,  Ldp2,  Lcm1,  Lcm2, Lcm3
              , Lls1,  Lls2,  Lrf1,  Lrf2
              , Wdp1,  Wdp2,  Wcm1,  Wcm2, Wcm3
              , Wls1,  Wls2,  Wrf1,  Wrf2
              , Mdp11, Mdp21, Mcm11, Mcm21, Mcm31, Mls11, Mls21, Mrf11, Mrf21
              , Mdp12, Mdp22, Mcm12, Mcm22, Mcm32, Mls12, Mls22
                            , Mcm13, Mcm23
                            , Mcm14, Mcm24
                            , Mcm25 ]

    sizing  = pd.DataFrame(np.array([values]), columns = keys)

    return sizing

def unscaler() -> tuple[ np.ndarray, np.ndarray, np.ndarray
                       , np.ndarray, np.ndarray ]:
    """ Upper and lower bounds and selection masks """
    x_min = np.array([ 5.0, 5.0, 5.0, 10.0, 1.0, 10.0, 1.0, 5.0, 5.0
                     , 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0, 7.0
                     , 3.0, 3.0, 3.0, 3.0, 1.0 ])
    x_max = np.array([ 15.0, 15.0, 15.0, 20.0, 10.0, 20.0, 10.0, 15.0, 15.0
                     , 9.0, 9.0, 9.0, 9.0, 9.0, 9.0, 9.0, 9.0, 9.0
                     , 9.0, 9.0, 9.0, 9.0, 6.0 ])
    gm    = np.array([(i in range(0,9))   for i in range(23)])
    fm    = np.array([(i in range(9,18))  for i in range(23)])
    im    = np.array([(i in range(18,23)) for i in range(23)])
    return (x_min, x_max, gm, fm, im)

def reference_goal(constraints: dict) -> np.ndarray:
    """ Curated Referece Goal for RFA """
    vdd = constraints.get('vdd', 1.8)
    return { "A":           1.0e-5
           , "a_0":         70.0
           , "ugbw":        2000000.0
           , "sr_r":        500000.0
           , "sr_f":        -500000.0
           , "pm":          80.0
           , "gm":          -65.0
           , "cmrr":        100.0 #120.0
           , "psrr_n":      100.0
           , "psrr_p":      100.0 # 125.0
           , "idd":         4.0e-05
           , "iss":         -4.0e-05
           , "vn_1Hz":      3.5e-06
           , "vn_10Hz":     1.0e-06
           , "vn_100Hz":    3.5e-07
           , "vn_1kHz":     1.0e-07
           , "vn_10kHz":    5.25e-08
           , "vn_100kHz":   4.5e-08
           , "cof":         400000000.0
           , "overshoot_r": 0.0005
           , "overshoot_f": 0.0005
           , "i_out_max":   1.5e-05
           , "i_out_min":   -1.5e-05
           , "v_ol":        (vdd * 0.45)
           , "v_oh":        (vdd * 0.55)
           , "v_il":        (vdd * 0.25)
           , "v_ih":        (vdd * 0.75)
           , "voff_stat":   0.002
           , "voff_sys":    -5.0e-06 }

def output_scale( constraints: dict
                ) -> tuple[dict[str, float], dict[str, float]]:
    """
    Estimated [-1.0;1.0] scaler for the Performance obtained from serafin.
    Arguments:
        - `constraints`: Design constraints obtained from serafin.
    """
    vdd = constraints.get('vdd', 1.8)
    x_min = { "a_0":         -120.0
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
    x_max = { "a_0":         100.0
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
    return (x_min, x_max)
