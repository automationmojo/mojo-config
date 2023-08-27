"""
.. module:: normalize
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module that contains functions for normalizing configuraiton environment parameters.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

from typing import List

import os


def normalize_name_list(names: str, sep: str=",") -> List[str]:
    norm_names: List[str] = []

    cand_names: List[str] = names.split(sep)
    for nxt_name in cand_names:
        nname = nxt_name.strip()
        norm_names.append(nname)

    return norm_names


def normalize_source_list(sources: str, sep: str=";") -> List[str]:
    norm_sources: List[str] = []

    search_sources: List[str] = sources.split(sep)
    for nxtsrc in search_sources:
        norm_sources.append(nxtsrc.strip())

    return norm_sources
