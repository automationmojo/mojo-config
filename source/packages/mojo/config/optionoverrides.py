__author__ = "Myron Walker"
__copyright__ = "Copyright 2020, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"

from typing import List

from datetime import datetime

from mojo.collections.contextpaths import ContextPaths
from mojo.collections.wellknown import ContextSingleton

from mojo.config.normalize import normalize_path_list
from mojo.config.overrides import MOJO_CONFIG_OVERRIDES
from mojo.config.variables import MOJO_CONFIG_VARIABLES


ctx = ContextSingleton()

class MOJO_CONFIG_OPTION_OVERRIDES:

    @staticmethod
    def override_config_credentials_names(credential_names: List[str]):
        """
            This override function provides a mechanism overriding the MJR_CONFIG_CREDENTIALS_NAMES
            variable and context configuration setting.

            :param landscape_names: The names of the credential configs to use when creating the credential config.
        """
        ctx.insert(ContextPaths.CONFIG_CREDENTIAL_NAMES, credential_names)
        MOJO_CONFIG_VARIABLES.MJR_CONFIG_CREDENTIAL_NAMES = credential_names
        MOJO_CONFIG_VARIABLES.MJR_CONFIG_USE_CREDENTIALS = True
        return

    @staticmethod
    def override_config_credentials_sources(sources: List[str]):
        """
            This override function provides a mechanism overriding the MJR_CONFIG_CREDENTIALS_SOURCES
            variable and context configuration setting.

            :param sources: The uri(s) of to use as the credential config search uri(s).
        """
        ctx.insert(ContextPaths.CONFIG_CREDENTIAL_SOURCES, sources)
        MOJO_CONFIG_VARIABLES.MJR_CONFIG_CREDENTIAL_SOURCES = sources
        return

    @staticmethod
    def override_config_credentials_files(filepaths: List[str]):
        """
            The override function used to override the MJR_CONFIG_CREDENTIAL_FILES variable and update
            the context configuration setting.

            :param filepaths: A list of file paths for configuration files.
        """
        filepaths = normalize_path_list(filepaths)
        ctx.insert(ContextPaths.CONFIG_CREDENTIAL_FILES, filepaths)
        MOJO_CONFIG_VARIABLES.MJR_CONFIG_CREDENTIAL_FILES = filepaths
        return

    @staticmethod
    def override_config_landscape_names(landscape_names: List[str]):
        """
            This override function provides a mechanism overriding the MJR_CONFIG_LANDSCAPE_NAMES
            variable and context configuration setting.

            :param landscape_names: The names of the landscape configs to use when creating the landscape config.
        """
        ctx.insert(ContextPaths.CONFIG_LANDSCAPE_NAMES, landscape_names)
        MOJO_CONFIG_VARIABLES.MJR_CONFIG_LANDSCAPE_NAMES = landscape_names
        MOJO_CONFIG_VARIABLES.MJR_CONFIG_USE_LANDSCAPE = True
        return

    @staticmethod
    def override_config_landscape_sources(sources: List[str]):
        """
            This override function provides a mechanism overriding the MJR_CONFIG_LANDSCAPE_SOURCES
            variable and context configuration setting.

            :param sources: The uri(s) of to use as the landscape config search uri(s).
        """
        ctx.insert(ContextPaths.CONFIG_LANDSCAPE_SOURCES, sources)
        MOJO_CONFIG_VARIABLES.MJR_CONFIG_LANDSCAPE_SOURCES = sources
        return

    @staticmethod
    def override_config_landscape_files(filepaths: List[str]):
        """
            The override function used to override the MJR_CONFIG_LANDSCAPE_FILES variable and update
            the context configuration setting.

            :param filepaths: A list of file paths for configuration files.
        """
        filepaths = normalize_path_list(filepaths)
        ctx.insert(ContextPaths.CONFIG_LANDSCAPE_FILES, filepaths)
        MOJO_CONFIG_VARIABLES.MJR_CONFIG_LANDSCAPE_FILES = filepaths
        return

    @staticmethod
    def override_config_runtime_names(runtime_names: List[str]):
        """
            This override function provides a mechanism overriding the MJR_CONFIG_RUNTIME_NAMES
            variable and context configuration setting.

            :param runtime_names: The names of the runtime files to use when selecting runtime files.
        """
        ctx.insert(ContextPaths.CONFIG_RUNTIME_NAMES, runtime_names)
        MOJO_CONFIG_VARIABLES.MJR_CONFIG_RUNTIME_NAMES = runtime_names
        MOJO_CONFIG_VARIABLES.MJR_CONFIG_USE_RUNTIME = True
        return

    @staticmethod
    def override_config_runtime_sources(sources: List[str]):
        """
            This override function provides a mechanism overriding the MJR_CONFIG_RUNTIME_SOURCES
            variable and context configuration setting.

            :param sources: The uri(s) of to use as the runtime config search uri(s).

        """
        ctx.insert(ContextPaths.CONFIG_RUNTIME_SOURCES, sources)
        MOJO_CONFIG_VARIABLES.MJR_CONFIG_RUNTIME_SOURCES = sources
        return

    @staticmethod
    def override_config_runtime_files(filepaths: List[str]):
        """
            The override function used to override the MJR_CONFIG_RUNTIME_FILES variable and update
            the context configuration setting.

            :param filepaths: A list of file paths for configuration files.
        """
        filepaths = normalize_path_list(filepaths)
        ctx.insert(ContextPaths.CONFIG_RUNTIME_FILES, filepaths)
        MOJO_CONFIG_VARIABLES.MJR_CONFIG_RUNTIME_FILES = filepaths
        return


    @staticmethod
    def override_config_topology_names(topology_names: List[str]):
        """
            This override function provides a mechanism overriding the MJR_CONFIG_TOPOLOGY_NAMES
            variable and context configuration setting.

            :param topology_names: The names of the topology files to use when selecting topology files.
        """
        ctx.insert(ContextPaths.CONFIG_TOPOLOGY_NAMES, topology_names)
        MOJO_CONFIG_VARIABLES.MJR_CONFIG_TOPOLOGY_NAMES = topology_names
        MOJO_CONFIG_VARIABLES.MJR_CONFIG_USE_TOPOLOGY = True
        return

    @staticmethod
    def override_config_topology_sources(sources: List[str]):
        """
            This override function provides a mechanism overriding the MJR_CONFIG_TOPOLOGY_SOURCES
            variable and context configuration setting.

            :param sources: The uri(s) of to use as the topology config search uri(s).
        """
        ctx.insert(ContextPaths.CONFIG_TOPOLOGY_SOURCES, sources)
        MOJO_CONFIG_VARIABLES.MJR_CONFIG_TOPOLOGY_SOURCES = sources
        return

    @staticmethod
    def override_config_topology_files(filepaths: List[str]):
        """
            The override function used to override the MJR_CONFIG_TOPOLOGY_FILES variable and update
            the context configuration setting.

            :param filepaths: A list of file paths for configuration files.
        """
        filepaths = normalize_path_list(filepaths)
        ctx.insert(ContextPaths.CONFIG_TOPOLOGY_FILES, filepaths)
        MOJO_CONFIG_VARIABLES.MJR_CONFIG_TOPOLOGY_FILES = filepaths
        return

    @staticmethod
    def override_configuration_requirements(require_credentials: bool,
            require_landscape: bool, require_runtime: bool, require_topology: bool):
        """
            Called before or after activating the runtime in order to modify the required configuration
            files based on the applicaiton or run requirements.

            :param require_credentials: Indicates a credentials configuration file is required.
            :param require_landscape: Indicates a landscape configuration file is required.
            :param require_runtime: Indicates a runtime configuration file is required.
            :param require_topology: Indicates a topology configuration file is required.
        """

        MOJO_CONFIG_OVERRIDES.MJR_CONFIG_REQUIRE_CREDENTIALS = require_credentials
        MOJO_CONFIG_OVERRIDES.MJR_CONFIG_REQUIRE_LANDSCAPE = require_landscape
        MOJO_CONFIG_OVERRIDES.MJR_CONFIG_REQUIRE_RUNTIME = require_runtime
        MOJO_CONFIG_OVERRIDES.MJR_CONFIG_REQUIRE_TOPOLOGY = require_topology

        return
