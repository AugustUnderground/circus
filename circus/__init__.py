""" Circus Gym Registry """

from gym.envs.registration import register
from .circus import *

## XH035-3V3
# AC²E: OP1 - Miller Operational Amplifier
register( id          = 'op1-xh035-geom-v0'
        , entry_point = 'circus.gym:OP1XH035GeomV0'
        , )
register( id          = 'op1-xh035-geom-v1'
        , entry_point = 'circus.gym:OP1XH035GeomV1'
        , )
register( id          = 'op1-xh035-elec-v0'
        , entry_point = 'circus.gym:OP1XH035ElecV0'
        , )
register( id          = 'op1-xh035-elec-v1'
        , entry_point = 'circus.gym:OP1XH035ElecV1'
        , )
# AC²E: OP2 - Symmetrical Amplifier
register( id          = 'op2-xh035-geom-v0'
        , entry_point = 'circus.gym:OP2XH035GeomV0'
        , )
register( id          = 'op2-xh035-geom-v1'
        , entry_point = 'circus.gym:OP2XH035GeomV1'
        , )
register( id          = 'op2-xh035-elec-v0'
        , entry_point = 'circus.gym:OP2XH035ElecV0'
        , )
register( id          = 'op2-xh035-elec-v1'
        , entry_point = 'circus.gym:OP2XH035ElecV1'
        , )
# AC²E: OP8 - Folded Cascode
register( id          = 'op8-xh035-geom-v0'
        , entry_point = 'circus.gym:OP8XH035GeomV0'
        , )
register( id          = 'op8-xh035-geom-v1'
        , entry_point = 'circus.gym:OP8XH035GeomV1'
        , )
register( id          = 'op8-xh035-elec-v0'
        , entry_point = 'circus.gym:OP8XH035ElecV0'
        , )
register( id          = 'op8-xh035-elec-v1'
        , entry_point = 'circus.gym:OP8XH035ElecV1'
        , )

## XH018-1V8
# AC²E: OP1 - Miller Operational Amplifier
register( id          = 'op1-xh018-geom-v0'
        , entry_point = 'circus.gym:OP1XH018GeomV0'
        , )
register( id          = 'op1-xh018-geom-v1'
        , entry_point = 'circus.gym:OP1XH018GeomV1'
        , )
register( id          = 'op1-xh018-elec-v0'
        , entry_point = 'circus.gym:OP1XH018ElecV0'
        , )
register( id          = 'op1-xh018-elec-v1'
        , entry_point = 'circus.gym:OP1XH018ElecV1'
        , )
# AC²E: OP2 - Symmetrical Amplifier
register( id          = 'op2-xh018-geom-v0'
        , entry_point = 'circus.gym:OP2XH018GeomV0'
        , )
register( id          = 'op2-xh018-geom-v1'
        , entry_point = 'circus.gym:OP2XH018GeomV1'
        , )
register( id          = 'op2-xh018-elec-v0'
        , entry_point = 'circus.gym:OP2XH018ElecV0'
        , )
register( id          = 'op2-xh018-elec-v1'
        , entry_point = 'circus.gym:OP2XH018ElecV1'
        , )
# AC²E: OP8 - Folded Cascode
register( id          = 'op8-xh018-geom-v0'
        , entry_point = 'circus.gym:OP8XH018GeomV0'
        , )
register( id          = 'op8-xh018-geom-v1'
        , entry_point = 'circus.gym:OP8XH018GeomV1'
        , )
register( id          = 'op8-xh018-elec-v0'
        , entry_point = 'circus.gym:OP8XH018ElecV0'
        , )
register( id          = 'op8-xh018-elec-v1'
        , entry_point = 'circus.gym:OP8XH018ElecV1'
        , )
