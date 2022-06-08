"""Reward Functions"""

from typing import Any, List, Optional, Type, Union, Callable
import numpy as np

def dummy_reward(observation: np.ndarray) -> np.ndarray:
    """ Default reward function for non-goal environments (v1).
    Arguments: `observation`
    Returns: `reward`
    """
    return np.sum(observation['observation'], axis = 1)

def binary_reward( predicate: list[Callable], observation: dict[str, np.ndarray]
                 , ) -> np.ndarray:
    """ Default reward function for goal environments (v0).
    Arguments:  `predicate`, `observation`
    Returns: `reward` in {-1;0}
    """
    desired_goal  = observation['desired_goal']
    achieved_goal = observation['achieved_goal']
    return np.all( np.stack([ (p(a,d) if (a is not None) and (d is not None)
                                      else False)
                              for p,a,d in zip( predicate
                                              , list(achieved_goal.T)
                                              , list(desired_goal.T))
                            ]).T
                 , axis = 1) - 1.0
