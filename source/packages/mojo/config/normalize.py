"""
.. module:: normalize
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module that contains functions for normalizing configuraiton environment parameters.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

from typing import List

import os

SEPARATOR = ";"

mime_source_prefixes = [
    "http://",
    "https://",
    "dir://",
    "mongodb://"
]

def starts_with_mime_prefix(uri: str):
    swmp = False

    for prefix in mime_source_prefixes:
        if uri.startswith(prefix):
            swmp = True
            break

    return swmp

def normalize_source_path_list(paths: List[str]):
    norm_paths: List[str] = []

    for nxt_path in paths:
        if not starts_with_mime_prefix(nxt_path):
            nxt_full_path = os.path.abspath(os.path.expandvars(os.path.expanduser(nxt_path.strip())))
            norm_paths.append(nxt_full_path)
        else:
            norm_paths.append(nxt_path)

    return norm_paths

def normalize_file_path_list(paths: List[str]):
    norm_paths: List[str] = []

    for nxt_path in paths:
        if nxt_path.startswith("file://"):
            nxt_path = nxt_path.replace("file://", "", 1)

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
    norm_paths = normalize_file_path_list(paths)

    return norm_paths

def split_and_normalize_source_list(sources_val: str, sep: str=SEPARATOR) -> List[str]:

    search_sources: List[str] = sources_val.split(sep)
    norm_sources = normalize_source_path_list(search_sources)

    return norm_sources
