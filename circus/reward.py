"""Reward Functions"""

from typing import Any, List, Optional, Type, Union, Callable
import numpy as np

def default_reward(observation: np.array) -> np.array:
    """ Default reward function for non-goal environments (v1).
    Arguments: `observation`
    Returns: `reward`
    """
    return np.sum(observation, axis = 1)

def binary_reward( predicate: [Callable]
                 , desired_goal: np.array
                 , achieved_goal: np.array
                 , ) -> np.array:
    """ Default reward function for goal environments (v0).
    Arguments:  `predicate`, `desired_goal`, `achieved_goal`
    Returns: `reward` in {-1;0}
    """
    return np.all( np.stack([ p(a,d) for p,a,d in zip( predicate
                                                     , list(achieved_goal.T)
                                                     , list(desired_goal.T))
                            ]).T
                 , axis = 1) - 1.0
