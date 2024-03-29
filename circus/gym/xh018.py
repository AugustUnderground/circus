""" XFAB - XH018 """

from .op import *

# MIL - Miller Operational Amplifier
class MILXH018GeomV0(OPGeomV0):
    """MIL: Miller Operational Amplifier Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "mil"
                        , pdk_id = "xh018"
                        , **kwargs )

class MILXH018GeomV1(OPGeomV1):
    """MIL: Miller Operational Amplifier Non-Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "mil"
                        , pdk_id = "xh018"
                        , **kwargs )

class MILXH018ElecV0(OPElecV0):
    """MIL: Miller Operational Amplifier Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "mil"
                        , pdk_id = "xh018"
                        , **kwargs )

class MILXH018ElecV1(OPElecV1):
    """MIL: Miller Operational Amplifier Non-Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "mil"
                        , pdk_id = "xh018"
                        , **kwargs )

# SYM - Symmetrical Amplifier
class SYMXH018GeomV0(OPGeomV0):
    """SYM: Symmetrical Amplifier Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "sym"
                        , pdk_id = "xh018"
                        , **kwargs )

class SYMXH018GeomV1(OPGeomV1):
    """SYM: Symmetrical Amplifier Non-Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "sym"
                        , pdk_id = "xh018"
                        , **kwargs )

class SYMXH018ElecV0(OPElecV0):
    """SYM: Symmetrical Amplifier Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "sym"
                        , pdk_id = "xh018"
                        , **kwargs )

class SYMXH018ElecV1(OPElecV1):
    """SYM: Symmetrical Amplifier Non-Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "sym"
                        , pdk_id = "xh018"
                        , **kwargs )

# FCA - Folded Cascode
class FCAXH018GeomV0(OPGeomV0):
    """FCA: Folded Cascode Amplifier Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "fca"
                        , pdk_id = "xh018"
                        , **kwargs )

class FCAXH018GeomV1(OPGeomV1):
    """FCA: Folded Cascode Amplifier Non-Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "fca"
                        , pdk_id = "xh018"
                        , **kwargs )

class FCAXH018ElecV0(OPElecV0):
    """FCA: Folded Cascode Amplifier Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "fca"
                        , pdk_id = "xh018"
                        , **kwargs )

class FCAXH018ElecV1(OPElecV1):
    """FCA: Folded Cascode Amplifier Non-Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "fca"
                        , pdk_id = "xh018"
                        , **kwargs )

# RFA - Rail-To-Rail Folded-Cascode with Wide-Swing Current Mirror
class RFAXH018GeomV0(OPGeomV0):
    """RFA: Rail-To-Rail Folded Cascode Amplifier Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "rfa"
                        , pdk_id = "xh018"
                        , **kwargs )

class RFAXH018GeomV1(OPGeomV1):
    """RFA: Rail-To-Rail Folded Cascode Amplifier Non-Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "rfa"
                        , pdk_id = "xh018"
                        , **kwargs )

class RFAXH018ElecV0(OPElecV0):
    """RFA: Rail-To-Rail Folded Cascode Amplifier Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "rfa"
                        , pdk_id = "xh018"
                        , **kwargs )

class RFAXH018ElecV1(OPElecV1):
    """RFA: Rail-To-Rail Folded Cascode Amplifier Non-Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "rfa"
                        , pdk_id = "xh018"
                        , **kwargs )
