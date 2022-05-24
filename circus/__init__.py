""" Circus Module """

from gym.envs.registration import register
from .circus import *

# AC²E: OP2 - Symmetrical Amplifier
register( id          = 'op2-xh035-geom-v0'
        , entry_point = 'circus.ckt:OP2XH035Geom'
        , )
