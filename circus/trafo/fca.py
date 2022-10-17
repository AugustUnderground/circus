"""
Agnostic Design Space Transforation for FCA: Folded Cascode Amplifier

`INPUTS` are:

    [ 'MNCM11_gmoverid', 'MPCM21_gmoverid', 'MNCM31_gmoverid'
    , 'MNLS11_gmoverid', 'MNLS21_gmoverid', 'MNDP11_gmoverid'
    , 'MNCM11_fug',      'MPCM21_fug',      'MNCM31_fug'
    , 'MNLS11_fug',      'MNLS21_fug',      'MNDP11_fug'
    , 'MNCM12_id',       'MNCM23_id' ]
"""

from fractions import Fraction
import numpy as np
import torch as pt
import pandas as pd

INPUTS: [str] = [ 'MNCM11_gmoverid', 'MPCM21_gmoverid', 'MNCM31_gmoverid'
                , 'MNLS11_gmoverid', 'MNLS21_gmoverid', 'MNDP11_gmoverid'
                , 'MNCM11_fug',      'MPCM21_fug',      'MNCM31_fug'
                , 'MNLS11_fug',      'MNLS21_fug',      'MNDP11_fug'
                , 'MNCM12_id',       'MNCM23_id' ]

def transform( constraints: dict, nmos: pt.nn.Module, pmos: pt.nn.Module
             , gmid_cm1: float, gmid_cm2: float, gmid_cm3: float
             , gmid_ls1: float, gmid_ls2: float, gmid_dp1: float
             , fug_cm1: float,  fug_cm2: float,  fug_cm3: float
             , fug_ls1: float,  fug_ls2: float,  fug_dp1: float
             , i1: float, i4: float ) -> pd.DataFrame:
    """ Electrical to Geometrical Transforation for FCA """

    i2      = i1
    i3      = (i1 / 2.0) + i4

    i0      = constraints.get('i0',   3e-6)
    vdd     = constraints.get('vsup', 1.8)

    M1_lim  = int(constraints.get('Mcm13', 42))
    M2_lim  = int(constraints.get('Mcm23', 42))

    W1_lim  = float(constraints.get('width', {}).get('max', 100e-6))
    W2_lim  = float(constraints.get('width', {}).get('max', 100e-6))
    W3_lim  = float(constraints.get('width', {}).get('max', 100e-6))

    M1      = Fraction(i0 / i1).limit_denominator(M1_lim)
    M2      = Fraction(i2 / i3).limit_denominator(M2_lim)

    Mdp11   = constraints.get('Mdp11', 2)
    Mdp12   = constraints.get('Mdp11', Mdp11)

    Mcm11   = max(M1.numerator, 1)
    Mcm12   = Mcm13 = max(M1.denominator, 1)
    Mcm21   = max(M2.numerator, 1)
    Mcm22   = Mcm23 = max(M2.denominator, 1)

    cm1_in  = pt.Tensor([[gmid_cm1, fug_cm1,  (vdd / 5.0),         0.0 ]])
    cm2_in  = pt.Tensor([[gmid_cm2, fug_cm2,  (vdd / 3.5), -(vdd / 5.0)]])
    cm3_in  = pt.Tensor([[gmid_cm3, fug_cm3, -(vdd / 3.0),  (vdd / 5.0)]])
    ls1_in  = pt.Tensor([[gmid_ls1, fug_ls1, -(vdd / 3.5),         0.0 ]])
    ls2_in  = pt.Tensor([[gmid_ls2, fug_ls2,  (vdd / 4.5),         0.0 ]])
    dp1_in  = pt.Tensor([[gmid_dp1, fug_dp1,  (vdd / 2.0), -(vdd / 4.5)]])

    cm1_out = nmos(cm1_in).numpy()[0]
    cm2_out = nmos(cm2_in).numpy()[0]
    cm3_out = pmos(cm3_in).numpy()[0]
    ls1_out = pmos(ls1_in).numpy()[0]
    ls2_out = nmos(ls2_in).numpy()[0]
    dp1_out = nmos(dp1_in).numpy()[0]

    Lcm1    = cm1_out[1]
    Lcm2    = cm2_out[1]
    Lcm3    = cm3_out[1]
    Lls1    = ls1_out[1]
    Lls2    = ls2_out[1]
    Ldp1    = dp1_out[1]

    Wl1     = i4 / ls1_out[0]
    Wl2     = i4 / ls2_out[0]
    Wc3     = i4 / cm3_out[0]
    Mls11   = Mls12 = np.ceil(Wl1 / W1_lim).item()
    Mls21   = Mls22 = np.ceil(Wl2 / W2_lim).item()
    Mcm31   = Mcm32 = np.ceil(Wc3 / W3_lim).item()
    Wls1    = Wl1 / Mls11
    Wls2    = Wl2 / Mls21
    Wcm3    = Wc3 / Mcm31

    Wcm1    = i0       / cm1_out[0] / Mcm11
    Wcm2    = i2       / cm2_out[0] / Mcm21
    Wdp1    = i1 / 2.0 / dp1_out[0] / Mdp11

    keys = [ 'Ldp1',  'Lcm1',  'Lcm2',  'Lcm3',  'Lls1',  'Lls2'
           , 'Wdp1',  'Wcm1',  'Wcm2',  'Wcm3',  'Wls1',  'Wls2'
           , 'Mdp11', 'Mcm11', 'Mcm21', 'Mcm31', 'Mls11', 'Mls21'
           , 'Mdp12', 'Mcm12', 'Mcm22', 'Mcm32', 'Mls12', 'Mls22'
                    , 'Mcm13', 'Mcm23' ]

    values  = [ Ldp1,  Lcm1,  Lcm2,  Lcm3,  Lls1,  Lls2
              , Wdp1,  Wcm1,  Wcm2,  Wcm3,  Wls1,  Wls2
              , Mdp11, Mcm11, Mcm21, Mcm31, Mls11, Mls21
              , Mdp12, Mcm12, Mcm22, Mcm32, Mls12, Mls22
                     , Mcm13, Mcm23 ]

    sizing  = pd.DataFrame(np.array([values]), columns = keys)

    return sizing

def unscaler() -> tuple[ np.ndarray, np.ndarray, np.ndarray
                       , np.ndarray, np.ndarray]:
    """ Upper and lower bounds and selection masks """
    x_min = np.array([ 5.0, 5.0, 5.0, 5.0, 5.0, 5.0
                     , 7.0, 7.0, 7.0, 7.0, 7.0, 7.0
                     , 1.0, 3.0 ])
    x_max = np.array([ 15.0, 15.0, 15.0, 15.0, 15.0, 15.0
                     , 9.0, 9.0, 9.0, 9.0, 9.0, 9.0
                     , 6.0, 9.0 ])
    gm    = np.array([(i in range(0,6))   for i in range(14)])
    fm    = np.array([(i in range(6,12))  for i in range(14)])
    im    = np.array([(i in range(12,14)) for i in range(14)])
    return (x_min, x_max, gm, fm, im)

def reference_goal(constraints: dict) -> np.ndarray:
    """ Curated Referece Goal for FCA """
    vdd   = constraints.get('vdd', 1.8)
    return { 'area':      5.5e-10      # 8.35135e-10
           , 'a_0':       65.0         # 65.50825257646494
           , 'ugbw':      750.0e3      # 608137.1389850643
           , 'sr_r':      750.0e3      # 482568.7087129002
           , 'sr_f':      750.0e3      # -478544.5088903557
           , 'pm':        80.0         # 89.13695404645551
           , 'gm':        -65.0        # -67.66169835915815
           , 'cmrr':      120.0        # 162.47373336546218
           , 'psrr_n':    100.0        # 100.13765587162408
           , 'psrr_p':    120.0        # 129.22912741937355
           , 'idd':       1.75e-5      # 1.5197106684950545e-05
           , 'iss':       -2.0e-5      # -1.8197106699045546e-05
           , 'vn_1Hz':    1.5e-5       # 1.6051837422213292e-05
           , 'vn_10Hz':   4.5e-6       # 4.7505758803117315e-06
           , 'vn_100Hz':  1.5e-6       # 1.397702658168099e-06
           , 'vn_1kHz':   4.0e-7       # 4.1657014801681973e-07
           , 'vn_10kHz':  1.5e-7       # 1.5526276209235358e-07
           , 'vn_100kHz': 1.0e-7       # 1.0126074486509364e-07
           , 'cof':       300.0e6      # 281341676.572598
           , 'os_r':      250.0e-6     # 0.0002498645125906737
           , 'os_f':      250.0e-6     # 0.0002738703385872967
           , 'i_out_min': -6.0e-6      # -6.031772879587186e-06
           , 'i_out_max': 8.5e-6       # 8.675972745540758e-06
           , 'v_ol':      (vdd * 0.45) # 1.5877847742499538
           , 'v_oh':      (vdd * 0.50) # 1.7122234338584263
           , 'v_il':      (vdd * 0.22) # 0.7476786622011943
           , 'v_ih':      (vdd * 1.00) # 3.7814460160662557
           , 'voff_stat': 5.0e-3       # 0.0072408778584526915
           , 'voff_syst': -5.0e-7      # -4.817662030216676e-07
           , }

def output_scale( constraints: dict
                ) -> tuple[dict[str, float], dict[str, float]]:
    """
    Used by `performance_scale` to scale performance obtained from serafin s.t.
    ∈ [-1,1].
    """
    vdd = constraints.get('vdd', 1.8)
    x_min = { 'a_0':       25.0
            , 'ugbw':      5.0
            , 'pm':        0.0
            , 'gm':        0.0
            , 'sr_r':      4.0
            , 'sr_f':      4.0
            , 'vn_1Hz':    -10.0
            , 'vn_10Hz':   -10.0
            , 'vn_100Hz':  -10.0
            , 'vn_1kHz':   -10.0
            , 'vn_10kHz':  -10.0
            , 'vn_100kHz': -10.0
            , 'cmrr':      70
            , 'psrr_n':    30.0
            , 'psrr_p':    40.0
            , 'v_il':      0.0
            , 'v_ih':      0.0
            , 'v_ol':      0.0
            , 'v_oh':      0.0
            , 'i_out_min': -6.0
            , 'i_out_max': -6.0
            , 'idd':       -6.0
            , 'iss':       -6.0
            , 'os_r':      0.0
            , 'os_f':      0.0
            , 'cof':       5.0
            , 'voff_stat': -5.0
            , 'voff_syst':  -5.0
            , 'area':      -15.0
            , }
    x_max = { 'a_0':       70.0
            , 'ugbw':      10.0
            , 'pm':        120.0
            , 'gm':        80.0
            , 'sr_r':      8.0
            , 'sr_f':      8.0
            , 'vn_1Hz':    -4.0
            , 'vn_10Hz':   -4.0
            , 'vn_100Hz':  -4.0
            , 'vn_1kHz':   -4.0
            , 'vn_10kHz':  -4.0
            , 'vn_100kHz': -4.0
            , 'cmrr':      150.0
            , 'psrr_n':    70.0
            , 'psrr_p':    140.0
            , 'v_il':      (2.0 * vdd)
            , 'v_ih':      (2.0 * vdd)
            , 'v_ol':      (2.0 * vdd)
            , 'v_oh':      (2.0 * vdd)
            , 'i_out_min': -3.0
            , 'i_out_max': -3.0
            , 'idd':       -3.0
            , 'iss':       -3.0
            , 'os_r':      130.0
            , 'os_f':      130.0
            , 'cof':       9.0
            , 'voff_stat': 0.0
            , 'voff_syst': 0.0
            , 'area':      -5.0
            , }
    return (x_min, x_max)
