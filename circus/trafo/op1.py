""" Agnostic Design Space Transforation for OP1: Miller Operational Amplifier """

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
    """ Transforation for OP1 """

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
    Mcm13   = (M1.numerator * M3.denominator) // M3.numerator

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

def unscaler(ace_backend: str) -> Callable:
    """ Unscale function for a given PDK """
    x_min = np.array([5.0,  5.0,  5.0,  5.0,  6.0, 6.0, 6.0, 6.0, 10.0, 40.0])
    x_max = np.array([15.0, 15.0, 15.0, 15.0, 9.0, 9.0, 9.0, 9.0, 30.0, 80.0])
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
