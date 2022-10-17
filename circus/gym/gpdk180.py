""" XFAB - GPDK180 """

from .op import *

# MIL - Miller Operational Amplifier
class MILGPDK180GeomV0(OPGeomV0):
    """MIL: Miller Operational Amplifier Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "mil"
                        , pdk_id = "gpdk180"
                        , **kwargs )

class MILGPDK180GeomV1(OPGeomV1):
    """MIL: Miller Operational Amplifier Non-Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "mil"
                        , pdk_id = "gpdk180"
                        , **kwargs )

class MILGPDK180ElecV0(OPElecV0):
    """MIL: Miller Operational Amplifier Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "mil"
                        , pdk_id = "gpdk180"
                        , **kwargs )

class MILGPDK180ElecV1(OPElecV1):
    """MIL: Miller Operational Amplifier Non-Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "mil"
                        , pdk_id = "gpdk180"
                        , **kwargs )

# SYM - Symmetrical Amplifier
class SYMGPDK180GeomV0(OPGeomV0):
    """SYM: Symmetrical Amplifier Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "sym"
                        , pdk_id = "gpdk180"
                        , **kwargs )

class SYMGPDK180GeomV1(OPGeomV1):
    """SYM: Symmetrical Amplifier Non-Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "sym"
                        , pdk_id = "gpdk180"
                        , **kwargs )

class SYMGPDK180ElecV0(OPElecV0):
    """SYM: Symmetrical Amplifier Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "sym"
                        , pdk_id = "gpdk180"
                        , **kwargs )

class SYMGPDK180ElecV1(OPElecV1):
    """SYM: Symmetrical Amplifier Non-Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "sym"
                        , pdk_id = "gpdk180"
                        , **kwargs )

# FCA - Folded Cascode
class FCAGPDK180GeomV0(OPGeomV0):
    """FCA: Folded Cascode Amplifier Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "fca"
                        , pdk_id = "gpdk180"
                        , **kwargs )

class FCAGPDK180GeomV1(OPGeomV1):
    """FCA: Folded Cascode Amplifier Non-Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "fca"
                        , pdk_id = "gpdk180"
                        , **kwargs )

class FCAGPDK180ElecV0(OPElecV0):
    """FCA: Folded Cascode Amplifier Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "fca"
                        , pdk_id = "gpdk180"
                        , **kwargs )

class FCAGPDK180ElecV1(OPElecV1):
    """FCA: Folded Cascode Amplifier Non-Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "fca"
                        , pdk_id = "gpdk180"
                        , **kwargs )

# RFA - Rail-To-Rail Folded-Cascode with Wide-Swing Current Mirror
class RFAGPDK180GeomV0(OPGeomV0):
    """RFA: Rail-To-Rail Folded Cascode Amplifier Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "rfa"
                        , pdk_id = "gpdk180"
                        , **kwargs )

class RFAGPDK180GeomV1(OPGeomV1):
    """RFA: Rail-To-Rail Folded Cascode Amplifier Non-Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "rfa"
                        , pdk_id = "gpdk180"
                        , **kwargs )

class RFAGPDK180ElecV0(OPElecV0):
    """RFA: Rail-To-Rail Folded Cascode Amplifier Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "rfa"
                        , pdk_id = "gpdk180"
                        , **kwargs )

class RFAGPDK180ElecV1(OPElecV1):
    """RFA: Rail-To-Rail Folded Cascode Amplifier Non-Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ckt_id = "rfa"
                        , pdk_id = "gpdk180"
                        , **kwargs )
