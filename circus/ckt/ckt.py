"""Circuit Sizing Environments (for gym registry)"""

from collections import OrderedDict
import numpy as np

from ..circus import CircusGeom, CircusGeomVec

class OPGeomV0(CircusGeom):
    """OP Geometric Goal Env Base"""
    def __init__(self, num_steps: int = 50, **kwargs):
        super().__init__(**kwargs)

    def reset(self, **kwargs):
        obs = super().reset(**kwargs)
        return OrderedDict({ k: v[0] for k,v in obs.items() })

    def step(self, action: np.array):
        dim     = self.action_space.shape[0]
        a       = np.reshape(action, [1,dim])
        o,r,d,i = super().step(a)
        obs     = OrderedDict({ k: v[0] for k,v in o.items() })
        return (obs, r.item(), d.item(), i[0])

class OPGeomV1(CircusGeomVec):
    """OP Geometric Non-Goal Env Base"""
    def __init__(self, num_steps: int = 50, **kwargs):
        super().__init__(**kwargs)

    def reset(self, **kwargs) -> np.ndarray:
        return super().reset(**kwargs)[0]

    def step(self, action: np.array) -> tuple[np.array, float, bool, dict[str, [str]]]:
        dim     = self.action_space.shape[0]
        a       = np.reshape(action, [1,dim])
        o,r,d,i = super().step(a)
        return (o[0], r.item(), d.item(), i[0])

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
