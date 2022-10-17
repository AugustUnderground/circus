""" XFAB - GPDK090 """

from .op import *

# MIL - Miller Operational Amplifier
class MILGPDK090GeomV0(OPGeomV0):
    """MIL: Miller Operational Amplifier Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "mil"
                        , pdk_id = "gpdk090"
                        , **kwargs )

class MILGPDK090GeomV1(OPGeomV1):
    """MIL: Miller Operational Amplifier Non-Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "mil"
                        , pdk_id = "gpdk090"
                        , **kwargs )

class MILGPDK090ElecV0(OPElecV0):
    """MIL: Miller Operational Amplifier Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "mil"
                        , pdk_id = "gpdk090"
                        , **kwargs )

class MILGPDK090ElecV1(OPElecV1):
    """MIL: Miller Operational Amplifier Non-Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "mil"
                        , pdk_id = "gpdk090"
                        , **kwargs )

# SYM - Symmetrical Amplifier
class SYMGPDK090GeomV0(OPGeomV0):
    """SYM: Symmetrical Amplifier Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "sym"
                        , pdk_id = "gpdk090"
                        , **kwargs )

class SYMGPDK090GeomV1(OPGeomV1):
    """SYM: Symmetrical Amplifier Non-Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "sym"
                        , pdk_id = "gpdk090"
                        , **kwargs )

class SYMGPDK090ElecV0(OPElecV0):
    """SYM: Symmetrical Amplifier Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "sym"
                        , pdk_id = "gpdk090"
                        , **kwargs )

class SYMGPDK090ElecV1(OPElecV1):
    """SYM: Symmetrical Amplifier Non-Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "sym"
                        , pdk_id = "gpdk090"
                        , **kwargs )

# FCA - Folded Cascode
class FCAGPDK090GeomV0(OPGeomV0):
    """FCA: Folded Cascode Amplifier Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "fca"
                        , pdk_id = "gpdk090"
                        , **kwargs )

class FCAGPDK090GeomV1(OPGeomV1):
    """FCA: Folded Cascode Amplifier Non-Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "fca"
                        , pdk_id = "gpdk090"
                        , **kwargs )

class FCAGPDK090ElecV0(OPElecV0):
    """FCA: Folded Cascode Amplifier Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "fca"
                        , pdk_id = "gpdk090"
                        , **kwargs )

class FCAGPDK090ElecV1(OPElecV1):
    """FCA: Folded Cascode Amplifier Non-Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "fca"
                        , pdk_id = "gpdk090"
                        , **kwargs )

# RFA - Rail-To-Rail Folded-Cascode with Wide-Swing Current Mirror
class RFAGPDK090GeomV0(OPGeomV0):
    """RFA: Rail-To-Rail Folded Cascode Amplifier Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "rfa"
                        , pdk_id = "gpdk090"
                        , **kwargs )

class RFAGPDK090GeomV1(OPGeomV1):
    """RFA: Rail-To-Rail Folded Cascode Amplifier Non-Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "rfa"
                        , pdk_id = "gpdk090"
                        , **kwargs )

class RFAGPDK090ElecV0(OPElecV0):
    """RFA: Rail-To-Rail Folded Cascode Amplifier Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "rfa"
                        , pdk_id = "gpdk090"
                        , **kwargs )

class RFAGPDK090ElecV1(OPElecV1):
    """RFA: Rail-To-Rail Folded Cascode Amplifier Non-Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "rfa"
                        , pdk_id = "gpdk090"
                        , **kwargs )
