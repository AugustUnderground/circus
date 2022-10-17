""" Gym compatible Analog Circuit Environment """

from gym.envs.registration import register
from .circus import *

## XH035-3V3
# AC²E: MIL - Miller Operational Amplifier
# register( id          = 'mil-xh035-geom-v0'
#         , entry_point = 'circus.gym:MILXH035GeomV0'
#         , )
# register( id          = 'mil-xh035-geom-v1'
#         , entry_point = 'circus.gym:MILXH035GeomV1'
#         , )
# register( id          = 'mil-xh035-elec-v0'
#         , entry_point = 'circus.gym:MILXH035ElecV0'
#         , )
# register( id          = 'mil-xh035-elec-v1'
#         , entry_point = 'circus.gym:MILXH035ElecV1'
#         , )
# # AC²E: SYM - Symmetrical Amplifier
# register( id          = 'sym-xh035-geom-v0'
#         , entry_point = 'circus.gym:SYMXH035GeomV0'
#         , )
# register( id          = 'sym-xh035-geom-v1'
#         , entry_point = 'circus.gym:SYMXH035GeomV1'
#         , )
# register( id          = 'sym-xh035-elec-v0'
#         , entry_point = 'circus.gym:SYMXH035ElecV0'
#         , )
# register( id          = 'sym-xh035-elec-v1'
#         , entry_point = 'circus.gym:SYMXH035ElecV1'
#         , )
# # AC²E: FCA - Folded Cascode
# register( id          = 'fca-xh035-geom-v0'
#         , entry_point = 'circus.gym:FCAXH035GeomV0'
#         , )
# register( id          = 'fca-xh035-geom-v1'
#         , entry_point = 'circus.gym:FCAXH035GeomV1'
#         , )
# register( id          = 'fca-xh035-elec-v0'
#         , entry_point = 'circus.gym:FCAXH035ElecV0'
#         , )
# register( id          = 'fca-xh035-elec-v1'
#         , entry_point = 'circus.gym:FCAXH035ElecV1'
#         , )
# # AC²E: RFA - Rail-To-Rail Folded-Cascode with Wide-Swing Current Mirror
# register( id          = 'rfa-xh035-geom-v0'
#         , entry_point = 'circus.gym:FCAXH035GeomV0'
#         , )
# register( id          = 'rfa-xh035-geom-v1'
#         , entry_point = 'circus.gym:FCAXH035GeomV1'
#         , )
# register( id          = 'rfa-xh035-elec-v0'
#         , entry_point = 'circus.gym:FCAXH035ElecV0'
#         , )
# register( id          = 'rfa-xh035-elec-v1'
#         , entry_point = 'circus.gym:FCAXH035ElecV1'
#         , )

## XH018
# MIL - Miller Operational Amplifier
register( id          = 'mil-xh018-geom-v0'
        , entry_point = 'circus.gym:MILXH018GeomV0'
        , )
register( id          = 'mil-xh018-geom-v1'
        , entry_point = 'circus.gym:MILXH018GeomV1'
        , )
register( id          = 'mil-xh018-elec-v0'
        , entry_point = 'circus.gym:MILXH018ElecV0'
        , )
register( id          = 'mil-xh018-elec-v1'
        , entry_point = 'circus.gym:MILXH018ElecV1'
        , )
# SYM - Symmetrical Amplifier
register( id          = 'sym-xh018-geom-v0'
        , entry_point = 'circus.gym:SYMXH018GeomV0'
        , )
register( id          = 'sym-xh018-geom-v1'
        , entry_point = 'circus.gym:SYMXH018GeomV1'
        , )
register( id          = 'sym-xh018-elec-v0'
        , entry_point = 'circus.gym:SYMXH018ElecV0'
        , )
register( id          = 'sym-xh018-elec-v1'
        , entry_point = 'circus.gym:SYMXH018ElecV1'
        , )
# FCA - Folded Cascode
register( id          = 'fca-xh018-geom-v0'
        , entry_point = 'circus.gym:FCAXH018GeomV0'
        , )
register( id          = 'fca-xh018-geom-v1'
        , entry_point = 'circus.gym:FCAXH018GeomV1'
        , )
register( id          = 'fca-xh018-elec-v0'
        , entry_point = 'circus.gym:FCAXH018ElecV0'
        , )
register( id          = 'fca-xh018-elec-v1'
        , entry_point = 'circus.gym:FCAXH018ElecV1'
        , )
# RFA - Rail-To-Rail Folded-Cascode with Wide-Swing Current Mirror
register( id          = 'rfa-xh018-geom-v0'
        , entry_point = 'circus.gym:RFAXH018GeomV0'
        , )
register( id          = 'rfa-xh018-geom-v1'
        , entry_point = 'circus.gym:RFAXH018GeomV1'
        , )
register( id          = 'rfa-xh018-elec-v0'
        , entry_point = 'circus.gym:RFAXH018ElecV0'
        , )
register( id          = 'rfa-xh018-elec-v1'
        , entry_point = 'circus.gym:RFAXH018ElecV1'
        , )

## XT018
# MIL - Miller Operational Amplifier
register( id          = 'mil-xt018-geom-v0'
        , entry_point = 'circus.gym:MILXT018GeomV0'
        , )
register( id          = 'mil-xt018-geom-v1'
        , entry_point = 'circus.gym:MILXT018GeomV1'
        , )
register( id          = 'mil-xt018-elec-v0'
        , entry_point = 'circus.gym:MILXT018ElecV0'
        , )
register( id          = 'mil-xt018-elec-v1'
        , entry_point = 'circus.gym:MILXT018ElecV1'
        , )
# SYM - Symmetrical Amplifier
register( id          = 'sym-xt018-geom-v0'
        , entry_point = 'circus.gym:SYMXT018GeomV0'
        , )
register( id          = 'sym-xt018-geom-v1'
        , entry_point = 'circus.gym:SYMXT018GeomV1'
        , )
register( id          = 'sym-xt018-elec-v0'
        , entry_point = 'circus.gym:SYMXT018ElecV0'
        , )
register( id          = 'sym-xt018-elec-v1'
        , entry_point = 'circus.gym:SYMXT018ElecV1'
        , )
# FCA - Folded Cascode Amplifier
register( id          = 'fca-xt018-geom-v0'
        , entry_point = 'circus.gym:FCAXT018GeomV0'
        , )
register( id          = 'fca-xt018-geom-v1'
        , entry_point = 'circus.gym:FCAXT018GeomV1'
        , )
register( id          = 'fca-xt018-elec-v0'
        , entry_point = 'circus.gym:FCAXT018ElecV0'
        , )
register( id          = 'fca-xt018-elec-v1'
        , entry_point = 'circus.gym:FCAXT018ElecV1'
        , )
# RFA - Rail-To-Rail Folded-Cascode with Wide-Swing Current Mirror
register( id          = 'rfa-xt018-geom-v0'
        , entry_point = 'circus.gym:RFAXT018GeomV0'
        , )
register( id          = 'rfa-xt018-geom-v1'
        , entry_point = 'circus.gym:RFAXT018GeomV1'
        , )
register( id          = 'rfa-xt018-elec-v0'
        , entry_point = 'circus.gym:RFAXT018ElecV0'
        , )
register( id          = 'rfa-xt018-elec-v1'
        , entry_point = 'circus.gym:RFAXT018ElecV1'
        , )

## GPDK180
# MIL - Miller Operational Amplifier
register( id          = 'mil-gpdk180-geom-v0'
        , entry_point = 'circus.gym:MILGPDK180GeomV0'
        , )
register( id          = 'mil-gpdk180-geom-v1'
        , entry_point = 'circus.gym:MILGPDK180GeomV1'
        , )
register( id          = 'mil-gpdk180-elec-v0'
        , entry_point = 'circus.gym:MILGPDK180ElecV0'
        , )
register( id          = 'mil-gpdk180-elec-v1'
        , entry_point = 'circus.gym:MILGPDK180ElecV1'
        , )
# SYM - Symmetrical Amplifier
register( id          = 'sym-gpdk180-geom-v0'
        , entry_point = 'circus.gym:SYMGPDK180GeomV0'
        , )
register( id          = 'sym-gpdk180-geom-v1'
        , entry_point = 'circus.gym:SYMGPDK180GeomV1'
        , )
register( id          = 'sym-gpdk180-elec-v0'
        , entry_point = 'circus.gym:SYMGPDK180ElecV0'
        , )
register( id          = 'sym-gpdk180-elec-v1'
        , entry_point = 'circus.gym:SYMGPDK180ElecV1'
        , )
# FCA - Folded Cascode Amplifier
register( id          = 'fca-gpdk180-geom-v0'
        , entry_point = 'circus.gym:FCAGPDK180GeomV0'
        , )
register( id          = 'fca-gpdk180-geom-v1'
        , entry_point = 'circus.gym:FCAGPDK180GeomV1'
        , )
register( id          = 'fca-gpdk180-elec-v0'
        , entry_point = 'circus.gym:FCAGPDK180ElecV0'
        , )
register( id          = 'fca-gpdk180-elec-v1'
        , entry_point = 'circus.gym:FCAGPDK180ElecV1'
        , )
# RFA - Rail-To-Rail Folded-Cascode with Wide-Swing Current Mirror
register( id          = 'rfa-gpdk180-geom-v0'
        , entry_point = 'circus.gym:RFAGPDK180GeomV0'
        , )
register( id          = 'rfa-gpdk180-geom-v1'
        , entry_point = 'circus.gym:RFAGPDK180GeomV1'
        , )
register( id          = 'rfa-gpdk180-elec-v0'
        , entry_point = 'circus.gym:RFAGPDK180ElecV0'
        , )
register( id          = 'rfa-gpdk180-elec-v1'
        , entry_point = 'circus.gym:RFAGPDK180ElecV1'
        , )

## GPDK090
# MIL - Miller Operational Amplifier
register( id          = 'mil-gpdk090-geom-v0'
        , entry_point = 'circus.gym:MILGPDK090GeomV0'
        , )
register( id          = 'mil-gpdk090-geom-v1'
        , entry_point = 'circus.gym:MILGPDK090GeomV1'
        , )
register( id          = 'mil-gpdk090-elec-v0'
        , entry_point = 'circus.gym:MILGPDK090ElecV0'
        , )
register( id          = 'mil-gpdk090-elec-v1'
        , entry_point = 'circus.gym:MILGPDK090ElecV1'
        , )
# SYM - Symmetrical Amplifier
register( id          = 'sym-gpdk090-geom-v0'
        , entry_point = 'circus.gym:SYMGPDK090GeomV0'
        , )
register( id          = 'sym-gpdk090-geom-v1'
        , entry_point = 'circus.gym:SYMGPDK090GeomV1'
        , )
register( id          = 'sym-gpdk090-elec-v0'
        , entry_point = 'circus.gym:SYMGPDK090ElecV0'
        , )
register( id          = 'sym-gpdk090-elec-v1'
        , entry_point = 'circus.gym:SYMGPDK090ElecV1'
        , )
# FCA - Folded Cascode Amplifier
register( id          = 'fca-gpdk090-geom-v0'
        , entry_point = 'circus.gym:FCAGPDK090GeomV0'
        , )
register( id          = 'fca-gpdk090-geom-v1'
        , entry_point = 'circus.gym:FCAGPDK090GeomV1'
        , )
register( id          = 'fca-gpdk090-elec-v0'
        , entry_point = 'circus.gym:FCAGPDK090ElecV0'
        , )
register( id          = 'fca-gpdk090-elec-v1'
        , entry_point = 'circus.gym:FCAGPDK090ElecV1'
        , )
# RFA - Rail-To-Rail Folded-Cascode with Wide-Swing Current Mirror
register( id          = 'rfa-gpdk090-geom-v0'
        , entry_point = 'circus.gym:RFAGPDK090GeomV0'
        , )
register( id          = 'rfa-gpdk090-geom-v1'
        , entry_point = 'circus.gym:RFAGPDK090GeomV1'
        , )
register( id          = 'rfa-gpdk090-elec-v0'
        , entry_point = 'circus.gym:RFAGPDK090ElecV0'
        , )
register( id          = 'rfa-gpdk090-elec-v1'
        , entry_point = 'circus.gym:RFAGPDK090ElecV1'
        , )

## GPDK045
# MIL - Miller Operational Amplifier
register( id          = 'mil-gpdk045-geom-v0'
        , entry_point = 'circus.gym:MILGPDK045GeomV0'
        , )
register( id          = 'mil-gpdk045-geom-v1'
        , entry_point = 'circus.gym:MILGPDK045GeomV1'
        , )
register( id          = 'mil-gpdk045-elec-v0'
        , entry_point = 'circus.gym:MILGPDK045ElecV0'
        , )
register( id          = 'mil-gpdk045-elec-v1'
        , entry_point = 'circus.gym:MILGPDK045ElecV1'
        , )
# SYM - Symmetrical Amplifier
register( id          = 'sym-gpdk045-geom-v0'
        , entry_point = 'circus.gym:SYMGPDK045GeomV0'
        , )
register( id          = 'sym-gpdk045-geom-v1'
        , entry_point = 'circus.gym:SYMGPDK045GeomV1'
        , )
register( id          = 'sym-gpdk045-elec-v0'
        , entry_point = 'circus.gym:SYMGPDK045ElecV0'
        , )
register( id          = 'sym-gpdk045-elec-v1'
        , entry_point = 'circus.gym:SYMGPDK045ElecV1'
        , )
# FCA - Folded Cascode Amplifier
register( id          = 'fca-gpdk045-geom-v0'
        , entry_point = 'circus.gym:FCAGPDK045GeomV0'
        , )
register( id          = 'fca-gpdk045-geom-v1'
        , entry_point = 'circus.gym:FCAGPDK045GeomV1'
        , )
register( id          = 'fca-gpdk045-elec-v0'
        , entry_point = 'circus.gym:FCAGPDK045ElecV0'
        , )
register( id          = 'fca-gpdk045-elec-v1'
        , entry_point = 'circus.gym:FCAGPDK045ElecV1'
        , )
# RFA - Rail-To-Rail Folded-Cascode with Wide-Swing Current Mirror
register( id          = 'rfa-gpdk045-geom-v0'
        , entry_point = 'circus.gym:RFAGPDK045GeomV0'
        , )
register( id          = 'rfa-gpdk045-geom-v1'
        , entry_point = 'circus.gym:RFAGPDK045GeomV1'
        , )
register( id          = 'rfa-gpdk045-elec-v0'
        , entry_point = 'circus.gym:RFAGPDK045ElecV0'
        , )
register( id          = 'rfa-gpdk045-elec-v1'
        , entry_point = 'circus.gym:RFAGPDK045ElecV1'
        , )
