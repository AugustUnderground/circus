"""Circuit Sizing Environments"""

import gym
from gym.spaces import Dict, Box
import numpy as np

from ..circus import Circus

class OP1XH035Geom(Circus):
    """OP1: Symmetrical Amplifier"""
    def __init__(self, num_steps: int = 50):
        super().__init__( ace_id = "op1"
                        , ace_backend = "xh035-3V3"
                        , num_steps = num_steps)

class OP2XH035Geom(Circus):
    """OP2: Symmetrical Amplifier"""
    def __init__(self, num_steps: int = 50):
        super().__init__( ace_id = "op2"
                        , ace_backend = "xh035-3V3"
                        , num_steps = num_steps)

