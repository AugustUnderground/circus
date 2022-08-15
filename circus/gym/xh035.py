""" XH035 - 3V3 """

from .op import *

# AC²E: OP1 - Miller Operational Amplifier
class OP1XH035GeomV0(OPGeomV0):
    """OP1: Symmetrical Amplifier Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ace_id = "op1"
                        , ace_backend = "xh035-3V3"
                        , **kwargs )

class OP1XH035GeomV1(OPGeomV1):
    """OP1: Symmetrical Amplifier Non-Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ace_id = "op1"
                        , ace_backend = "xh035-3V3"
                        , **kwargs )

class OP1XH035ElecV0(OPElecV0):
    """OP1: Symmetrical Amplifier Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ace_id = "op1"
                        , ace_backend = "xh035-3V3"
                        , **kwargs )

class OP1XH035ElecV1(OPElecV1):
    """OP1: Symmetrical Amplifier Non-Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ace_id = "op1"
                        , ace_backend = "xh035-3V3"
                        , **kwargs )

# AC²E: OP2 - Symmetrical Amplifier
class OP2XH035GeomV0(OPGeomV0):
    """OP2: Symmetrical Amplifier Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ace_id = "op2"
                        , ace_backend = "xh035-3V3"
                        , **kwargs )

class OP2XH035GeomV1(OPGeomV1):
    """OP2: Symmetrical Amplifier Non-Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ace_id = "op2"
                        , ace_backend = "xh035-3V3"
                        , **kwargs )

class OP2XH035ElecV0(OPElecV0):
    """OP2: Symmetrical Amplifier Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ace_id = "op2"
                        , ace_backend = "xh035-3V3"
                        , **kwargs )

class OP2XH035ElecV1(OPElecV1):
    """OP2: Symmetrical Amplifier Non-Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ace_id = "op2"
                        , ace_backend = "xh035-3V3"
                        , **kwargs )

# AC²E: OP8 - Folded Cascode
class OP8XH035GeomV0(OPGeomV0):
    """OP8: Symmetrical Amplifier Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ace_id = "op8"
                        , ace_backend = "xh035-3V3"
                        , **kwargs )

class OP8XH035GeomV1(OPGeomV1):
    """OP8: Symmetrical Amplifier Non-Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ace_id = "op8"
                        , ace_backend = "xh035-3V3"
                        , **kwargs )

class OP8XH035ElecV0(OPElecV0):
    """OP8: Symmetrical Amplifier Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ace_id = "op8"
                        , ace_backend = "xh035-3V3"
                        , **kwargs )

class OP8XH035ElecV1(OPElecV1):
    """OP8: Symmetrical Amplifier Non-Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ace_id = "op8"
                        , ace_backend = "xh035-3V3"
                        , **kwargs )

# AC²E: OP11 - Rail-To-Rail Folded-Cascode with Wide-Swing Current Mirror
class OP11XH035GeomV0(OPGeomV0):
    """OP11: Symmetrical Amplifier Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ace_id = "op11"
                        , ace_backend = "xh035-3V3"
                        , **kwargs )

class OP11XH035GeomV1(OPGeomV1):
    """OP11: Symmetrical Amplifier Non-Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ace_id = "op11"
                        , ace_backend = "xh035-3V3"
                        , **kwargs )

class OP11XH035ElecV0(OPElecV0):
    """OP11: Symmetrical Amplifier Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ace_id = "op11"
                        , ace_backend = "xh035-3V3"
                        , **kwargs )

class OP11XH035ElecV1(OPElecV1):
    """OP11: Symmetrical Amplifier Non-Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ace_id = "op11"
                        , ace_backend = "xh035-3V3"
                        , **kwargs )
