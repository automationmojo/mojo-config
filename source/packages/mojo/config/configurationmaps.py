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

from mojo.collections.mergemap import MergeMap
from mojo.collections.context import Context, ContextPaths
from mojo.collections.wellknown import ContextSingleton

from mojo.config.overrides import MOJO_CONFIG_OVERRIDES
from mojo.config.variables import MOJO_CONFIG_VARNAMES, MOJO_CONFIG_VARIABLES

from mojo.config.configurationloader import ConfigurationLoader


CREDENTIALS_TABLE = None
LANDSCAPE_TABLE = None
RUNTIME_TABLE = None
TOPOLOGY_TABLE = None


class CONFIGURATION_MAPS:
    CREDENTIAL_CONFIGURATION_MAP = None
    LANDSCAPE_CONFIGURATION_MAP = None
    RUNTIME_CONFIGURATION_MAP = MergeMap(MOJO_CONFIG_OVERRIDES.DEFAULT_CONFIGURATION)
    TOPOLOGY_CONFIGURATION_MAP = None


def resolve_configuration_maps(
        use_credentials: Optional[bool]=None,
        use_landscape: Optional[bool]=None,
        use_runtime: Optional[bool]=None,
        use_topology: Optional[bool]=None,
        keyphrase: Optional[str]=None,
        credentials: Optional[Dict[str, Tuple[str, str]]] = None):

    if MOJO_CONFIG_VARNAMES.MJR_CONFIG_PASS_PHRASE in os.environ:
        MOJO_CONFIG_VARIABLES.MJR_CONFIG_PASS_PHRASE = os.environ[MOJO_CONFIG_VARNAMES.MJR_CONFIG_PASS_PHRASE]

    if keyphrase is not None:
        MOJO_CONFIG_VARIABLES.MJR_CONFIG_PASS_PHRASE = keyphrase
    else:
        keyphrase = MOJO_CONFIG_VARIABLES.MJR_CONFIG_PASS_PHRASE

    ctx = ContextSingleton()

    if use_credentials is not None:
        resolve_credentials_configuration(ctx, keyphrase=keyphrase, credentials=credentials)

    if use_landscape is not None:
        resolve_landscape_configuration(ctx, keyphrase=keyphrase, credentials=credentials)

    if use_runtime is not None:
        resolve_runtime_configuration(ctx, keyphrase=keyphrase, credentials=credentials)

    if use_topology is not None:
        resolve_topology_configuration(ctx, keyphrase=keyphrase, credentials=credentials)

    return


def resolve_credentials_configuration(ctx: Context, keyphrase: Optional[str] = None, credentials: Optional[Dict[str, Tuple[str, str]]] = None):

    global CREDENTIALS_TABLE

    MOJO_CONFIG_OVERRIDES.MJR_CONFIG_USE_CREDENTIALS = True

    MOJO_CONFIG_VARIABLES.MJR_CONFIG_CREDENTIAL_URIS = []
    if MOJO_CONFIG_OVERRIDES.MJR_CONFIG_USE_CREDENTIALS:
        config_names = MOJO_CONFIG_VARIABLES.MJR_CONFIG_CREDENTIAL_NAMES
        if len(config_names) == 0:
            config_names = ["credentials"]
        source_uris = MOJO_CONFIG_VARIABLES.MJR_CONFIG_CREDENTIAL_SOURCES

        config_loader = ConfigurationLoader(source_uris, credentials=credentials)

        CREDENTIALS_TABLE = OrderedDict()
        CONFIGURATION_MAPS.CREDENTIAL_CONFIGURATION_MAP = MergeMap()

        for cname in config_names:
            config_uri, config_info = config_loader.load_configuration(cname, keyphrase=keyphrase)
            CREDENTIALS_TABLE[config_uri] = config_info
            CONFIGURATION_MAPS.CREDENTIAL_CONFIGURATION_MAP.maps.insert(0, config_info)

        MOJO_CONFIG_VARIABLES.MJR_CONFIG_CREDENTIAL_URIS = [ cfguri for cfguri in  CREDENTIALS_TABLE.keys() ]

    ctx.insert(ContextPaths.CONFIG_CREDENTIAL_URIS, MOJO_CONFIG_VARIABLES.MJR_CONFIG_CREDENTIAL_URIS)

    return


def resolve_landscape_configuration(ctx: Context, keyphrase: Optional[str] = None, credentials: Optional[Dict[str, Tuple[str, str]]] = None):

    global LANDSCAPE_TABLE

    MOJO_CONFIG_OVERRIDES.MJR_CONFIG_USE_LANDSCAPE = True

    MOJO_CONFIG_VARIABLES.MJR_CONFIG_LANDSCAPE_URIS = []
    if MOJO_CONFIG_OVERRIDES.MJR_CONFIG_USE_LANDSCAPE:
        config_names = MOJO_CONFIG_VARIABLES.MJR_CONFIG_LANDSCAPE_NAMES
        if len(config_names) == 0:
            config_names = ["default-landscape"]
        source_uris = MOJO_CONFIG_VARIABLES.MJR_CONFIG_LANDSCAPE_SOURCES

        config_loader = ConfigurationLoader(source_uris, credentials=credentials)

        LANDSCAPE_TABLE = OrderedDict()
        CONFIGURATION_MAPS.LANDSCAPE_CONFIGURATION_MAP = MergeMap()

        for cname in config_names:
            config_uri, config_info = config_loader.load_configuration(cname, keyphrase=keyphrase)
            LANDSCAPE_TABLE[config_uri] = config_info
            CONFIGURATION_MAPS.LANDSCAPE_CONFIGURATION_MAP.maps.insert(0, config_info)

        MOJO_CONFIG_VARIABLES.MJR_CONFIG_LANDSCAPE_URIS = [ cfguri for cfguri in  LANDSCAPE_TABLE.keys() ]

    ctx.insert(ContextPaths.CONFIG_LANDSCAPE_URIS, MOJO_CONFIG_VARIABLES.MJR_CONFIG_LANDSCAPE_URIS)

    return


def resolve_runtime_configuration(ctx: Context, keyphrase: Optional[str] = None, credentials: Optional[Dict[str, Tuple[str, str]]] = None):

    global RUNTIME_TABLE

    MOJO_CONFIG_OVERRIDES.MJR_CONFIG_USE_RUNTIME = True

    MOJO_CONFIG_VARIABLES.MJR_CONFIG_RUNTIME_URIS = []
    if MOJO_CONFIG_OVERRIDES.MJR_CONFIG_USE_RUNTIME:
        config_names = MOJO_CONFIG_VARIABLES.MJR_CONFIG_RUNTIME_NAMES
        if len(config_names) == 0:
            config_names = ["default-runtime"]
        source_uris = MOJO_CONFIG_VARIABLES.MJR_CONFIG_RUNTIME_SOURCES

        config_loader = ConfigurationLoader(source_uris, credentials=credentials)

        RUNTIME_TABLE = OrderedDict()
        CONFIGURATION_MAPS.RUNTIME_CONFIGURATION_MAP = MergeMap()

        for cname in config_names:
            config_uri, config_info = config_loader.load_configuration(cname, keyphrase=keyphrase)
            RUNTIME_TABLE[config_uri] = config_info
            CONFIGURATION_MAPS.RUNTIME_CONFIGURATION_MAP.maps.insert(0, config_info)

        MOJO_CONFIG_VARIABLES.MJR_CONFIG_RUNTIME_URIS = [ cfguri for cfguri in  RUNTIME_TABLE.keys() ]

    ctx.insert(ContextPaths.CONFIG_RUNTIME_URIS, MOJO_CONFIG_VARIABLES.MJR_CONFIG_RUNTIME_URIS)

    return


def resolve_topology_configuration(ctx: Context, keyphrase: Optional[str] = None, credentials: Optional[Dict[str, Tuple[str, str]]] = None):

    global TOPOLOGY_TABLE

    MOJO_CONFIG_OVERRIDES.MJR_CONFIG_USE_TOPOLOGY = True

    MOJO_CONFIG_VARIABLES.MJR_CONFIG_TOPOLOGY_URIS = []
    if MOJO_CONFIG_OVERRIDES.MJR_CONFIG_USE_TOPOLOGY:
        config_names = MOJO_CONFIG_VARIABLES.MJR_CONFIG_TOPOLOGY_NAMES
        if len(config_names) == 0:
            config_names = ["default-topology"]
        source_uris = MOJO_CONFIG_VARIABLES.MJR_CONFIG_TOPOLOGY_SOURCES

        config_loader = ConfigurationLoader(source_uris, credentials=credentials)

        TOPOLOGY_TABLE = OrderedDict()
        CONFIGURATION_MAPS.TOPOLOGY_CONFIGURATION_MAP = MergeMap()

        for cname in config_names:
            config_uri, config_info = config_loader.load_configuration(cname, keyphrase=keyphrase)
            TOPOLOGY_TABLE[config_uri] = config_info
            CONFIGURATION_MAPS.TOPOLOGY_CONFIGURATION_MAP.maps.insert(0, config_info)

        MOJO_CONFIG_VARIABLES.MJR_CONFIG_TOPOLOGY_URIS = [ cfguri for cfguri in  TOPOLOGY_TABLE.keys() ]

    ctx.insert(ContextPaths.CONFIG_TOPOLOGY_URIS, MOJO_CONFIG_VARIABLES.MJR_CONFIG_TOPOLOGY_URIS)

    return

