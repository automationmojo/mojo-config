"""
.. module:: overrides
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module that contains an enumeration of environment variable names
               that are used by the configuration code.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2020, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"

import os

from mojo.startup.wellknown import StartupConfigSingleton

default_config = {}

startup_config = StartupConfigSingleton()
if "DEFAULT" in startup_config:
    default_config = startup_config["DEFAULT"]

class MOJO_CONFIG_OVERRIDES:

    MJR_CONFIG_REQUIRE_CREDENTIALS = False
    if "MJR_CONFIG_REQUIRE_CREDENTIALS" in default_config:
        MJR_CONFIG_REQUIRE_CREDENTIALS = default_config["MJR_CONFIG_REQUIRE_CREDENTIALS"]

    MJR_CONFIG_REQUIRE_LANDSCAPE = False
    if "MJR_CONFIG_REQUIRE_LANDSCAPE" in default_config:
        MJR_CONFIG_REQUIRE_LANDSCAPE = default_config["MJR_CONFIG_REQUIRE_LANDSCAPE"]

    MJR_CONFIG_REQUIRE_RUNTIME = False
    if "MJR_CONFIG_REQUIRE_RUNTIME" in default_config:
        MJR_CONFIG_REQUIRE_RUNTIME = default_config["MJR_CONFIG_REQUIRE_RUNTIME"]

    MJR_CONFIG_REQUIRE_TOPOLOGY = False
    if "MJR_CONFIG_REQUIRE_TOPOLOGY" in default_config:
        MJR_CONFIG_REQUIRE_TOPOLOGY = default_config["MJR_CONFIG_REQUIRE_TOPOLOGY"]

    DEFAULT_CONFIGURATION = {
        "version": "1.0.0",
        "logging": {
            "levels": {
                "console": "INFO",
                "logfile": "DEBUG"
            }
        }
    }
