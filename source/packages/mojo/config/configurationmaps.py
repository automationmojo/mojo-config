"""
.. module:: configurationmaps
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module that contains functions for searching for and loading different types of
               automation runtime configuration maps.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

from typing import Dict, Optional, Tuple

import os

from collections import OrderedDict

from mojo.collections.context import Context
from mojo.collections.contextpaths import ContextPaths
from mojo.collections.mergemap import MergeMap
from mojo.collections.wellknown import ContextSingleton


from mojo.config.variables import (
    MOJO_CONFIG_VARNAMES,
    MOJO_CONFIG_VARIABLES,
    CONFIGURATION_MAPS
)


from mojo.config.configurationloader import ConfigurationLoader


CREDENTIALS_TABLE = None
LANDSCAPE_TABLE = None
RUNTIME_TABLE = None
TOPOLOGY_TABLE = None


def resolve_configuration_maps(
        use_credentials: Optional[bool]=None,
        use_landscape: Optional[bool]=None,
        use_runtime: Optional[bool]=None,
        use_topology: Optional[bool]=None,
        keyphrase: Optional[str]=None,
        credentials: Optional[Dict[str, Tuple[str, str]]] = None):

    if use_credentials is None:
        use_credentials = MOJO_CONFIG_VARIABLES.MJR_CONFIG_USE_CREDENTIALS
    else:
        MOJO_CONFIG_VARIABLES.MJR_CONFIG_USE_CREDENTIALS = use_credentials

    if use_landscape is None:
        use_landscape = MOJO_CONFIG_VARIABLES.MJR_CONFIG_USE_LANDSCAPE
    else:
        MOJO_CONFIG_VARIABLES.MJR_CONFIG_USE_LANDSCAPE = use_landscape
    
    if use_runtime is None:
        use_runtime = MOJO_CONFIG_VARIABLES.MJR_CONFIG_USE_RUNTIME
    else:
        MOJO_CONFIG_VARIABLES.MJR_CONFIG_USE_RUNTIME = use_runtime
    
    if use_topology is None:
        use_topology = MOJO_CONFIG_VARIABLES.MJR_CONFIG_USE_TOPOLOGY
    else:
        MOJO_CONFIG_VARIABLES.MJR_CONFIG_USE_TOPOLOGY = use_topology

    if MOJO_CONFIG_VARNAMES.MJR_CONFIG_PASS_PHRASE in os.environ:
        MOJO_CONFIG_VARIABLES.MJR_CONFIG_PASS_PHRASE = os.environ[MOJO_CONFIG_VARNAMES.MJR_CONFIG_PASS_PHRASE]

    if keyphrase is not None:
        MOJO_CONFIG_VARIABLES.MJR_CONFIG_PASS_PHRASE = keyphrase
    else:
        keyphrase = MOJO_CONFIG_VARIABLES.MJR_CONFIG_PASS_PHRASE

    ctx = ContextSingleton()

    if use_credentials:
        resolve_credentials_configuration(ctx, keyphrase=keyphrase, credentials=credentials)

    if use_landscape:
        resolve_landscape_configuration(ctx, keyphrase=keyphrase, credentials=credentials)

    if use_runtime:
        resolve_runtime_configuration(ctx, keyphrase=keyphrase, credentials=credentials)

    if use_topology:
        resolve_topology_configuration(ctx, keyphrase=keyphrase, credentials=credentials)

    return


def resolve_credentials_configuration(ctx: Context, keyphrase: Optional[str] = None, credentials: Optional[Dict[str, Tuple[str, str]]] = None):

    global CREDENTIALS_TABLE

    CREDENTIALS_TABLE = OrderedDict()

    MOJO_CONFIG_VARIABLES.MJR_CONFIG_CREDENTIAL_URIS = []
    
    config_names = MOJO_CONFIG_VARIABLES.MJR_CONFIG_CREDENTIAL_NAMES
    config_files = MOJO_CONFIG_VARIABLES.MJR_CONFIG_CREDENTIAL_FILES

    if (config_names is None or len(config_names) == 0) and (config_files is None or len(config_files) == 0):
        MOJO_CONFIG_VARIABLES.MJR_CONFIG_CREDENTIAL_NAMES = ["credentials"]
        config_names = MOJO_CONFIG_VARIABLES.MJR_CONFIG_CREDENTIAL_NAMES

    if config_names is not None:
        source_uris = MOJO_CONFIG_VARIABLES.MJR_CONFIG_CREDENTIAL_SOURCES

        config_loader = ConfigurationLoader(source_uris, credentials=credentials)

        for cname in config_names:
            config_uri, config_info = config_loader.load_configuration_by_name(cname, keyphrase=keyphrase)
            CREDENTIALS_TABLE[config_uri] = config_info
            CONFIGURATION_MAPS.CREDENTIAL_CONFIGURATION_MAP.maps.insert(0, config_info)

        MOJO_CONFIG_VARIABLES.MJR_CONFIG_CREDENTIAL_URIS = [ cfguri for cfguri in  CREDENTIALS_TABLE.keys() ]

    if config_files is not None:
        config_loader = ConfigurationLoader([], credentials=credentials)
        for cfile in config_files:
            config_info = config_loader.load_configuration_from_file(cfile, keyphrase=keyphrase)
            CONFIGURATION_MAPS.CREDENTIAL_CONFIGURATION_MAP.maps.insert(0, config_info)

    ctx.insert(ContextPaths.CONFIG_CREDENTIAL_URIS, MOJO_CONFIG_VARIABLES.MJR_CONFIG_CREDENTIAL_URIS)

    return


def resolve_landscape_configuration(ctx: Context, keyphrase: Optional[str] = None, credentials: Optional[Dict[str, Tuple[str, str]]] = None):

    global LANDSCAPE_TABLE

    LANDSCAPE_TABLE = OrderedDict()

    MOJO_CONFIG_VARIABLES.MJR_CONFIG_LANDSCAPE_URIS = []
    CONFIGURATION_MAPS.LANDSCAPE_CONFIGURATION_MAP = MergeMap()
    
    config_names = MOJO_CONFIG_VARIABLES.MJR_CONFIG_LANDSCAPE_NAMES
    config_files = MOJO_CONFIG_VARIABLES.MJR_CONFIG_LANDSCAPE_FILES

    if (config_names is None or len(config_names) == 0) and (config_files is None or len(config_files) == 0):
        MOJO_CONFIG_VARIABLES.MJR_CONFIG_LANDSCAPE_NAMES = ["default-landscape"]
        config_names = MOJO_CONFIG_VARIABLES.MJR_CONFIG_LANDSCAPE_NAMES

    if config_names is not None:
        source_uris = MOJO_CONFIG_VARIABLES.MJR_CONFIG_LANDSCAPE_SOURCES

        config_loader = ConfigurationLoader(source_uris, credentials=credentials)

        for cname in config_names:
            config_uri, config_info = config_loader.load_configuration_by_name(cname, keyphrase=keyphrase)
            LANDSCAPE_TABLE[config_uri] = config_info
            CONFIGURATION_MAPS.LANDSCAPE_CONFIGURATION_MAP.maps.insert(0, config_info)

        MOJO_CONFIG_VARIABLES.MJR_CONFIG_LANDSCAPE_URIS = [ cfguri for cfguri in  LANDSCAPE_TABLE.keys() ]

    if config_files is not None:
        config_loader = ConfigurationLoader([], credentials=credentials)
        for cfile in config_files:
            config_info = config_loader.load_configuration_from_file(cfile, keyphrase=keyphrase)
            CONFIGURATION_MAPS.LANDSCAPE_CONFIGURATION_MAP.maps.insert(0, config_info)

    ctx.insert(ContextPaths.CONFIG_LANDSCAPE, CONFIGURATION_MAPS.LANDSCAPE_CONFIGURATION_MAP)
    ctx.insert(ContextPaths.CONFIG_LANDSCAPE_URIS, MOJO_CONFIG_VARIABLES.MJR_CONFIG_LANDSCAPE_URIS)

    return


def resolve_runtime_configuration(ctx: Context, keyphrase: Optional[str] = None, credentials: Optional[Dict[str, Tuple[str, str]]] = None):

    global RUNTIME_TABLE

    RUNTIME_TABLE = OrderedDict()

    MOJO_CONFIG_VARIABLES.MJR_CONFIG_RUNTIME_URIS = []
    CONFIGURATION_MAPS.RUNTIME_CONFIGURATION_MAP = MergeMap()

    config_names = MOJO_CONFIG_VARIABLES.MJR_CONFIG_RUNTIME_NAMES
    config_files = MOJO_CONFIG_VARIABLES.MJR_CONFIG_RUNTIME_FILES

    if (config_names is None or len(config_names) == 0) and (config_files is None or len(config_files) == 0):
        MOJO_CONFIG_VARIABLES.MJR_CONFIG_RUNTIME_NAMES = ["default-runtime"]
        config_names = MOJO_CONFIG_VARIABLES.MJR_CONFIG_RUNTIME_NAMES

    if config_names is not None:
        source_uris = MOJO_CONFIG_VARIABLES.MJR_CONFIG_RUNTIME_SOURCES

        config_loader = ConfigurationLoader(source_uris, credentials=credentials)

        for cname in config_names:
            config_uri, config_info = config_loader.load_configuration_by_name(cname, keyphrase=keyphrase)
            RUNTIME_TABLE[config_uri] = config_info
            CONFIGURATION_MAPS.RUNTIME_CONFIGURATION_MAP.maps.insert(0, config_info)

        MOJO_CONFIG_VARIABLES.MJR_CONFIG_RUNTIME_URIS = [ cfguri for cfguri in  RUNTIME_TABLE.keys() ]

    if config_files is not None:
        config_loader = ConfigurationLoader([], credentials=credentials)
        for cfile in config_files:
            config_info = config_loader.load_configuration_from_file(cfile, keyphrase=keyphrase)
            CONFIGURATION_MAPS.RUNTIME_CONFIGURATION_MAP.maps.insert(0, config_info)

    ctx.insert(ContextPaths.CONFIG_RUNTIME, CONFIGURATION_MAPS.RUNTIME_CONFIGURATION_MAP)
    ctx.insert(ContextPaths.CONFIG_RUNTIME_URIS, MOJO_CONFIG_VARIABLES.MJR_CONFIG_RUNTIME_URIS)

    return


def resolve_topology_configuration(ctx: Context, keyphrase: Optional[str] = None, credentials: Optional[Dict[str, Tuple[str, str]]] = None):

    global TOPOLOGY_TABLE

    TOPOLOGY_TABLE = OrderedDict()

    MOJO_CONFIG_VARIABLES.MJR_CONFIG_TOPOLOGY_URIS = []
    CONFIGURATION_MAPS.TOPOLOGY_CONFIGURATION_MAP = MergeMap()

    config_names = MOJO_CONFIG_VARIABLES.MJR_CONFIG_TOPOLOGY_NAMES
    config_files = MOJO_CONFIG_VARIABLES.MJR_CONFIG_TOPOLOGY_FILES

    if (config_names is None or len(config_names) == 0) and (config_files is None or len(config_files) == 0):
        MOJO_CONFIG_VARIABLES.MJR_CONFIG_TOPOLOGY_NAMES = ["default-topology"]
        config_names = MOJO_CONFIG_VARIABLES.MJR_CONFIG_TOPOLOGY_NAMES

    if config_names is not None:
        source_uris = MOJO_CONFIG_VARIABLES.MJR_CONFIG_TOPOLOGY_SOURCES

        config_loader = ConfigurationLoader(source_uris, credentials=credentials)

        for cname in config_names:
            config_uri, config_info = config_loader.load_configuration_by_name(cname, keyphrase=keyphrase)
            TOPOLOGY_TABLE[config_uri] = config_info
            CONFIGURATION_MAPS.TOPOLOGY_CONFIGURATION_MAP.maps.insert(0, config_info)

        MOJO_CONFIG_VARIABLES.MJR_CONFIG_TOPOLOGY_URIS = [ cfguri for cfguri in  TOPOLOGY_TABLE.keys() ]

    if config_files is not None:
        config_loader = ConfigurationLoader([], credentials=credentials)
        for cfile in config_files:
            config_info = config_loader.load_configuration_from_file(cfile, keyphrase=keyphrase)
            CONFIGURATION_MAPS.TOPOLOGY_CONFIGURATION_MAP.maps.insert(0, config_info)

    ctx.insert(ContextPaths.CONFIG_TOPOLOGY, CONFIGURATION_MAPS.TOPOLOGY_CONFIGURATION_MAP)
    ctx.insert(ContextPaths.CONFIG_TOPOLOGY_URIS, MOJO_CONFIG_VARIABLES.MJR_CONFIG_TOPOLOGY_URIS)

    return

