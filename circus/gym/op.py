""" Operational Amplifier Sizing Environments (for gym registry) """

from collections import OrderedDict
import numpy as np

from ..circus import CircusGeom, CircusGeomVec, CircusElec, CircusElecVec

class OPGeomV0(CircusGeom):
    """Generic OP Geometric Goal Env Base"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def reset(self, **kwargs):
        obs = super().reset(**kwargs)
        return OrderedDict({ k: v[0] for k,v in obs.items() })

    def step(self, actions: np.array):
        dim     = self.action_space.shape[0]
        a       = np.reshape(actions, [1,dim])
        o,r,d,i = super().step(a)
        obs     = OrderedDict({ k: v[0] for k,v in o.items() })
        return (obs, r.item(), d.item(), i[0])

class OPGeomV1(CircusGeomVec):
    """Generic OP Geometric Non-Goal Env Base"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def reset(self, **kwargs) -> np.ndarray:
        return super().reset(**kwargs)[0]

    def step( self, actions: np.array
            ) -> tuple[np.array, float, bool, dict[str, [str]]]:
        dim     = self.action_space.shape[0]
        a       = np.reshape(actions, [1,dim])
        o,r,d,i = super().step(a)
        return (o[0], r.item(), d.item(), i[0])

class OPElecV0(CircusElec):
    """Generic OP Geometric Goal Env Base"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def reset(self, **kwargs):
        obs = super().reset(**kwargs)
        return OrderedDict({ k: v[0] for k,v in obs.items() })

    def step(self, actions: np.array):
        dim     = self.action_space.shape[0]
        a       = np.reshape(actions, [1,dim])
        o,r,d,i = super().step(a)
        obs     = OrderedDict({ k: v[0] for k,v in o.items() })
        return (obs, r.item(), d.item(), i[0])

class OPElecV1(CircusElecVec):
    """Generic OP Geometric Non-Goal Env Base"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def reset(self, **kwargs) -> np.ndarray:
        return super().reset(**kwargs)[0]

    def step( self, actions: np.array
            ) -> tuple[np.array, float, bool, dict[str, [str]]]:
        dim     = self.action_space.shape[0]
        a       = np.reshape(actions, [1,dim])
        o,r,d,i = super().step(a)
        return (o[0], r.item(), d.item(), i[0])
