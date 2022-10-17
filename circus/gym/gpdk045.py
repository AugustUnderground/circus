""" XFAB - GPDK045 """

from .op import *

# MIL - Miller Operational Amplifier
class MILGPDK045GeomV0(OPGeomV0):
    """MIL: Miller Operational Amplifier Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "mil"
                        , pdk_id = "gpdk045"
                        , **kwargs )

class MILGPDK045GeomV1(OPGeomV1):
    """MIL: Miller Operational Amplifier Non-Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "mil"
                        , pdk_id = "gpdk045"
                        , **kwargs )

class MILGPDK045ElecV0(OPElecV0):
    """MIL: Miller Operational Amplifier Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "mil"
                        , pdk_id = "gpdk045"
                        , **kwargs )

class MILGPDK045ElecV1(OPElecV1):
    """MIL: Miller Operational Amplifier Non-Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "mil"
                        , pdk_id = "gpdk045"
                        , **kwargs )

# SYM - Symmetrical Amplifier
class SYMGPDK045GeomV0(OPGeomV0):
    """SYM: Symmetrical Amplifier Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "sym"
                        , pdk_id = "gpdk045"
                        , **kwargs )

class SYMGPDK045GeomV1(OPGeomV1):
    """SYM: Symmetrical Amplifier Non-Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "sym"
                        , pdk_id = "gpdk045"
                        , **kwargs )

class SYMGPDK045ElecV0(OPElecV0):
    """SYM: Symmetrical Amplifier Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "sym"
                        , pdk_id = "gpdk045"
                        , **kwargs )

class SYMGPDK045ElecV1(OPElecV1):
    """SYM: Symmetrical Amplifier Non-Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "sym"
                        , pdk_id = "gpdk045"
                        , **kwargs )

# FCA - Folded Cascode
class FCAGPDK045GeomV0(OPGeomV0):
    """FCA: Folded Cascode Amplifier Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "fca"
                        , pdk_id = "gpdk045"
                        , **kwargs )

class FCAGPDK045GeomV1(OPGeomV1):
    """FCA: Folded Cascode Amplifier Non-Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "fca"
                        , pdk_id = "gpdk045"
                        , **kwargs )

class FCAGPDK045ElecV0(OPElecV0):
    """FCA: Folded Cascode Amplifier Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "fca"
                        , pdk_id = "gpdk045"
                        , **kwargs )

class FCAGPDK045ElecV1(OPElecV1):
    """FCA: Folded Cascode Amplifier Non-Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "fca"
                        , pdk_id = "gpdk045"
                        , **kwargs )

# RFA - Rail-To-Rail Folded-Cascode with Wide-Swing Current Mirror
class RFAGPDK045GeomV0(OPGeomV0):
    """RFA: Rail-To-Rail Folded Cascode Amplifier Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "rfa"
                        , pdk_id = "gpdk045"
                        , **kwargs )

class RFAGPDK045GeomV1(OPGeomV1):
    """RFA: Rail-To-Rail Folded Cascode Amplifier Non-Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "rfa"
                        , pdk_id = "gpdk045"
                        , **kwargs )

class RFAGPDK045ElecV0(OPElecV0):
    """RFA: Rail-To-Rail Folded Cascode Amplifier Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "rfa"
                        , pdk_id = "gpdk045"
                        , **kwargs )

class RFAGPDK045ElecV1(OPElecV1):
    """RFA: Rail-To-Rail Folded Cascode Amplifier Non-Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "rfa"
                        , pdk_id = "gpdk045"
                        , **kwargs )
