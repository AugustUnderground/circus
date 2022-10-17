""" Serafin Parallel Processing Utilities """

import os
import operator
from typing import Any, List, Optional, Type, Union, Callable, Iterable
from multiprocessing.dummy import Pool

import numpy as np
import pandas as pd
import serafin as sf
import pyspectre as ps

def make_ops( ckt_cfg: str, pdk_cfg: str, netlist: str, num: int
            ) -> Iterable[sf.OperationalAmplifier]:
    """
    Create `num` op amp sessions, where `num` ∈ [1 .. ∞).
    Arguments:
        - `ckt_cfg`: path to `ckt_id.yml`
        - `pdk_cfg`: path to `pdk_id.yml`
        - `netlist`: path to `ckt_id.scs`
    Returns:
        - `list[serafin.OperationalAmplifier]`
    """
    # pdk_cfg = os.path.expanduser(f'~/.circus/pdk/{pdk_id}.yml')
    # ckt_cfg = os.path.expanduser(f'~/.circus/ckt/{ckt_id}.yml')
    # netlist = os.path.expanduser(f'~/.circus/pdk/{pdk_id}/{ckt_id}.scs')

    with Pool(num) as pl:
        args = zip(num * [pdk_cfg], num * [ckt_cfg], num * [netlist])
        ops  = pl.starmap(sf.operational_amplifier, args)

    return ops

def set_parameters( ops: Iterable[sf.OperationalAmplifier]
                  , sizing: Iterable[dict[str,float]] ) -> bool:
    """
    Set sizing parameters. Index in `sizing` list corresponds to index in `ops`
    list.
    """
    num = len(ops)
    with Pool(num) as pl:
        ret = pl.starmap( lambda o,s: ps.set_parameters(o.session, s)
                        , zip(ops, sizing) )
    return all(ret)

def current_sizing( ops: Iterable[sf.OperationalAmplifier] ) -> pd.DataFrame:
    """
    Retrieve the current sizing of all `ops`. Row index corresponds to index in
    `ops` list.
    """
    num = len(ops)
    with Pool(num) as pl:
        sizing = pd.concat(pl.map(sf.current_sizing, ops))
    return sizing

def random_sizing( ops: Iterable[sf.OperationalAmplifier] ) -> pd.DataFrame:
    """
    Get a random sizing for all `ops`. Row index corresponds to index in `ops`.
    """
    num = len(ops)
    with Pool(num) as pl:
        sizing = pd.concat(pl.map(sf.random_sizing, ops))
    return sizing

def evaluate( ops: Iterable[sf.OperationalAmplifier], sizing: pd.DataFrame
            ) -> pd.DataFrame:
    """
    Evaluate all `ops` in parallel. Row index of `sizing` must correspond with
    index in `ops`.
    """
    num     = len(ops)
    sizings = [row.to_frame().transpose() for _,row in sizing.iterrows()]
    with Pool(num) as pl:
        results = pd.concat(pl.starmap(sf.evaluate, zip(ops, sizings)))
    return results
