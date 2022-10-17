""" XFAB - XT018 """

from .op import *

# MIL - Miller Operational Amplifier
class MILXT018GeomV0(OPGeomV0):
    """MIL: Miller Operational Amplifier Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "mil"
                        , pdk_id = "xt018"
                        , **kwargs )

class MILXT018GeomV1(OPGeomV1):
    """MIL: Miller Operational Amplifier Non-Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "mil"
                        , pdk_id = "xt018"
                        , **kwargs )

class MILXT018ElecV0(OPElecV0):
    """MIL: Miller Operational Amplifier Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "mil"
                        , pdk_id = "xt018"
                        , **kwargs )

class MILXT018ElecV1(OPElecV1):
    """MIL: Miller Operational Amplifier Non-Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "mil"
                        , pdk_id = "xt018"
                        , **kwargs )

# SYM - Symmetrical Amplifier
class SYMXT018GeomV0(OPGeomV0):
    """SYM: Symmetrical Amplifier Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "sym"
                        , pdk_id = "xt018"
                        , **kwargs )

class SYMXT018GeomV1(OPGeomV1):
    """SYM: Symmetrical Amplifier Non-Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "sym"
                        , pdk_id = "xt018"
                        , **kwargs )

class SYMXT018ElecV0(OPElecV0):
    """SYM: Symmetrical Amplifier Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "sym"
                        , pdk_id = "xt018"
                        , **kwargs )

class SYMXT018ElecV1(OPElecV1):
    """SYM: Symmetrical Amplifier Non-Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "sym"
                        , pdk_id = "xt018"
                        , **kwargs )

# FCA - Folded Cascode
class FCAXT018GeomV0(OPGeomV0):
    """FCA: Folded Cascode Amplifier Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "fca"
                        , pdk_id = "xt018"
                        , **kwargs )

class FCAXT018GeomV1(OPGeomV1):
    """FCA: Folded Cascode Amplifier Non-Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "fca"
                        , pdk_id = "xt018"
                        , **kwargs )

class FCAXT018ElecV0(OPElecV0):
    """FCA: Folded Cascode Amplifier Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "fca"
                        , pdk_id = "xt018"
                        , **kwargs )

class FCAXT018ElecV1(OPElecV1):
    """FCA: Folded Cascode Amplifier Non-Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "fca"
                        , pdk_id = "xt018"
                        , **kwargs )

# RFA - Rail-To-Rail Folded-Cascode with Wide-Swing Current Mirror
class RFAXT018GeomV0(OPGeomV0):
    """RFA: Rail-To-Rail Folded Cascode Amplifier Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "rfa"
                        , pdk_id = "xt018"
                        , **kwargs )

class RFAXT018GeomV1(OPGeomV1):
    """RFA: Rail-To-Rail Folded Cascode Amplifier Non-Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "rfa"
                        , pdk_id = "xt018"
                        , **kwargs )

class RFAXT018ElecV0(OPElecV0):
    """RFA: Rail-To-Rail Folded Cascode Amplifier Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "rfa"
                        , pdk_id = "xt018"
                        , **kwargs )

class RFAXT018ElecV1(OPElecV1):
    """RFA: Rail-To-Rail Folded Cascode Amplifier Non-Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "rfa"
                        , pdk_id = "xt018"
                        , **kwargs )
