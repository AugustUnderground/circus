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
    vdd     = constraints.get('i0', {}).get('init', 3.3)

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

    cm1_in  = np.array([[gmid_cm1, fug_cm1,  (vdd / 4.0),       0.0 ]])
    cm2_in  = np.array([[gmid_cm2, fug_cm2, -(vdd / 3.0),       0.0 ]])
    cm3_in  = np.array([[gmid_cm3, fug_cm3,  (vdd / 4.0),       0.0 ]])
    dp1_in  = np.array([[gmid_dp1, fug_dp1,  (vdd / 3.0), -(vdd/4.0)]])

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

def unscaler(ace_backend: str) -> Callable:
    """ Unscale function for a given PDK """
    x_min = np.array([5.0,  5.0,  5.0,  5.0,  6.0, 6.0, 6.0, 6.0, 1.0,  1.0])
    x_max = np.array([15.0, 15.0, 15.0, 15.0, 9.0, 9.0, 9.0, 9.0, 30.0, 30.0])
    gm    = np.array([(i in range(0,4))  for i in range(10)])
    fm    = np.array([(i in range(4,8))  for i in range(10)])
    im    = np.array([(i in range(8,10)) for i in range(10)])
    def _unscale(x: np.array) -> np.array:
        y_ = x_min + ( ((np.vstack(x) + 1.0) / 2.0) * (x_max - x_min))
        y  = (y_ * gm) \
           + np.log10(y_ * fm, where = (y_ * fm) > 0.0) \
           + (y_ * im * 1e-6)
        return y
    return _unscale
