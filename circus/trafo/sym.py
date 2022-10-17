"""
Agnostic Design Space Transforation for SYM: Symmetrical Amplifier

`INPUTS` are:

    [ 'MNCM11_gmoverid', 'MPCM221_gmoverid', 'MNCM31_gmoverid', 'MND11_gmoverid'
    , 'MNCM11_fug',      'MPCM221_fug',      'MNCM31_fug',      'MND11_fug'
    , 'MNCM12_id',       'MNCM32_id' ]
"""

from fractions import Fraction
import numpy as np
import torch as pt
import pandas as pd

INPUTS: list[str] = [ 'MNCM11_gmoverid', 'MPCM221_gmoverid', 'MNCM31_gmoverid', 'MND11_gmoverid'
                    , 'MNCM11_fug',      'MPCM221_fug',      'MNCM31_fug',      'MND11_fug'
                    , 'MNCM12_id',       'MNCM32_id' ]

def transform( constraints: dict, nmos: pt.nn.Module, pmos: pt.nn.Module
             , gmid_cm1: float, gmid_cm2: float, gmid_cm4: float, gmid_dp1: float
             , fug_cm1: float,  fug_cm2: float,  fug_cm4: float,  fug_dp1: float
             , i1: float, i2: float ) -> dict[str, float]:
    """ Electrical to Geometrical Transforation for SYM """

    i0      = constraints.get('i0',  3e-6)
    vdd     = constraints.get('vdd', 1.8)

    M1_lim  = 42
    M2_lim  = 42

    M1      = Fraction(i0       / i1).limit_denominator(M1_lim)
    M2      = Fraction(i1 / 2.0 / i2).limit_denominator(M2_lim)

    Mcm11   = max(M1.numerator, 1)
    Mcm12   = max(M1.denominator, 1)
    Mcm21   = max(M2.numerator, 1)
    Mcm22   = max(M2.denominator, 1)

    Mdp11   = constraints.get('Mdp11', 2)
    Mdp12   = constraints.get('Mdp12', Mdp11)
    Mcm41   = constraints.get('Mcm41', 2)
    Mcm42   = constraints.get('Mcm42', 2)

    cm1_in  = pt.Tensor([[gmid_cm1, fug_cm1,  (vdd / 4.25),         0.00 ]])
    cm2_in  = pt.Tensor([[gmid_cm2, fug_cm2, -(vdd / 3.15),         0.00 ]])
    cm4_in  = pt.Tensor([[gmid_cm4, fug_cm4,  (vdd / 4.25),         0.00 ]])
    dp1_in  = pt.Tensor([[gmid_dp1, fug_dp1,  (vdd / 2.10), -(vdd / 4.85)]])

    cm1_out = nmos(cm1_in).numpy()[0]
    cm2_out = pmos(cm2_in).numpy()[0]
    cm4_out = nmos(cm4_in).numpy()[0]
    dp1_out = nmos(dp1_in).numpy()[0]

    Lcm1    = cm1_out[1]
    Lcm2    = cm2_out[1]
    Lcm4    = cm4_out[1]
    Ldp1    = dp1_out[1]

    Wcm1    = i0       / cm1_out[0] / Mcm11
    Wcm2    = i1 / 2.0 / cm2_out[0] / Mcm21
    Wcm4    = i2       / cm4_out[0] / Mcm41
    Wdp1    = i1 / 2.0 / dp1_out[0] / Mdp11

    Lcm3    = Lcm2
    Wcm3    = Wcm2
    Mcm31   = Mcm21
    Mcm32   = Mcm22

    keys    = [ 'Ldp1',  'Lcm1',  'Lcm2',  'Lcm3',  'Lcm4'
              , 'Wdp1',  'Wcm1',  'Wcm2',  'Wcm3',  'Wcm4'
              , 'Mdp11', 'Mcm11', 'Mcm21', 'Mcm31', 'Mcm41'
              , 'Mdp12', 'Mcm12', 'Mcm22', 'Mcm32', 'Mcm42' ]

    values  = [ Ldp1,  Lcm1,  Lcm2,  Lcm3,  Lcm4
              , Wdp1,  Wcm1,  Wcm2,  Wcm3,  Wcm4
              , Mdp11, Mcm11, Mcm21, Mcm31, Mcm41
              , Mdp12, Mcm12, Mcm22, Mcm32, Mcm42 ]

    sizing  = pd.DataFrame(np.array([values]), columns = keys)

    return sizing

def unscaler() -> tuple[ np.ndarray, np.ndarray, np.ndarray
                       , np.ndarray, np.ndarray ]:
    """ Upper and lower bounds and selection masks """
    x_min = np.array([5.0,  5.0,  5.0,  5.0,  7.0, 7.0, 7.0, 7.0, 1.0,  3.0])
    x_max = np.array([15.0, 15.0, 15.0, 15.0, 9.0, 9.0, 9.0, 9.0, 9.0, 15.0])
    gm    = np.array([(i in range(0,4))  for i in range(10)])
    fm    = np.array([(i in range(4,8))  for i in range(10)])
    im    = np.array([(i in range(8,10)) for i in range(10)])
    return (x_min, x_max, gm, fm, im)

def reference_goal(constraints: dict) -> np.ndarray:
    """ Curated Referece Goal for SYM """
    vdd = constraints.get('vdd', 1.8)
    return { "area":        5.0e-10      # 5.010925e-10
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
           , "os_r":        2.5          # 2.6405786027522846
           , "os_f":        2.0          # 2.152491375598402
           , "i_out_min":   -2.5e-5      # -2.34598447270796e-05
           , "i_out_max":   2.5e-5       # 2.375395528802124e-05
           , "v_ol":        (vdd * 0.50) # 1.6314814360399006
           , "v_oh":        (vdd * 0.95) # 1.6685034539424761
           , "v_il":        (vdd * 0.25) # 0.5688672464434619
           , "v_ih":        (vdd * 0.95) # 3.3502486012612174
           , "voff_stat":   3.0e-3       # 0.0031193237064727104
           , "voff_syst":   -1.5e-3      # -0.0015180853180561346
           , }

def output_scale( constraints: dict
                ) -> tuple[dict[str, float], dict[str,float]]:
    """ Extimated Min/Max values for scaling 'perf' """
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
