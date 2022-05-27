""" XH018 - 1V8 """

from .op import *

# AC²E: OP1 - Miller Operational Amplifier
class OP1XH018GeomV0(OPGeomV0):
    """OP1: Symmetrical Amplifier Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ace_id = "op1"
                        , ace_backend = "xh018-1V8"
                        , **kwargs )

class OP1XH018GeomV1(OPGeomV1):
    """OP1: Symmetrical Amplifier Non-Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ace_id = "op1"
                        , ace_backend = "xh018-1V8"
                        , **kwargs )

class OP1XH018ElecV0(OPElecV0):
    """OP1: Symmetrical Amplifier Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ace_id = "op1"
                        , ace_backend = "xh018-1V8"
                        , **kwargs )

class OP1XH018ElecV1(OPElecV1):
    """OP1: Symmetrical Amplifier Non-Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ace_id = "op1"
                        , ace_backend = "xh018-1V8"
                        , **kwargs )

# AC²E: OP2 - Symmetrical Amplifier
class OP2XH018GeomV0(OPGeomV0):
    """OP2: Symmetrical Amplifier Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ace_id = "op2"
                        , ace_backend = "xh018-1V8"
                        , **kwargs )

class OP2XH018GeomV1(OPGeomV1):
    """OP2: Symmetrical Amplifier Non-Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ace_id = "op2"
                        , ace_backend = "xh018-1V8"
                        , **kwargs )

class OP2XH018ElecV0(OPElecV0):
    """OP2: Symmetrical Amplifier Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ace_id = "op2"
                        , ace_backend = "xh018-1V8"
                        , **kwargs )

class OP2XH018ElecV1(OPElecV1):
    """OP2: Symmetrical Amplifier Non-Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ace_id = "op2"
                        , ace_backend = "xh018-1V8"
                        , **kwargs )

# AC²E: OP8 - Folded Cascode
class OP8XH018GeomV0(OPGeomV0):
    """OP8: Symmetrical Amplifier Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ace_id = "op8"
                        , ace_backend = "xh018-1V8"
                        , **kwargs )

class OP8XH018GeomV1(OPGeomV1):
    """OP8: Symmetrical Amplifier Non-Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ace_id = "op8"
                        , ace_backend = "xh018-1V8"
                        , **kwargs )

class OP8XH018ElecV0(OPElecV0):
    """OP8: Symmetrical Amplifier Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ace_id = "op8"
                        , ace_backend = "xh018-1V8"
                        , **kwargs )

class OP8XH018ElecV1(OPElecV1):
    """OP8: Symmetrical Amplifier Non-Goal Env"""
    def __init__(self, **kwargs):
        super().__init__( ace_id = "op8"
                        , ace_backend = "xh018-1V8"
                        , **kwargs )
