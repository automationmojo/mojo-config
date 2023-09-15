"""
.. module:: normalize
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module that contains functions for normalizing configuraiton environment parameters.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

from typing import List

import os

SEPARATOR = ";"

def normalize_path_list(paths: List[str]):
    norm_paths: List[str] = []

    for nxt_path in paths:
        nxt_full_path = os.path.abspath(os.path.expandvars(os.path.expanduser(nxt_path.strip())))
        norm_paths.append(nxt_full_path)

    return norm_paths

def split_and_normalize_name_list(names_val: str, sep: str=SEPARATOR) -> List[str]:
    norm_names: List[str] = []

    cand_names: List[str] = names_val.split(sep)
    for nxt_name in cand_names:
        nname = nxt_name.strip()
        norm_names.append(nname)

    return norm_names


def split_and_normalize_path_list(paths_val: str, sep: str=SEPARATOR):

    paths: List[str] = paths_val.split(sep)
    norm_paths = normalize_path_list(paths)

    return norm_paths

def split_and_normalize_source_list(sources_val: str, sep: str=SEPARATOR) -> List[str]:

    search_sources: List[str] = sources_val.split(sep)
    norm_sources = normalize_path_list(search_sources)

    return norm_sources
