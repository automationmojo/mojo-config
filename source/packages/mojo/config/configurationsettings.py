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


from typing import Optional

from mojo.startup.wellknown import StartupConfigSingleton
from mojo.startup.presencesettings import establish_presence_settings

default_config = {}

config = StartupConfigSingleton()
if "MOJO-CONFIG" in config:
    default_config = config["MOJO-CONFIG"]

class MOJO_CONFIG_DEFAULTS:

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

    MJR_CONFIG_STORAGE_URI = ""
    if "MJR_CONFIG_STORAGE_URI" in default_config:
        MJR_CONFIG_STORAGE_URI = default_config["MJR_CONFIG_STORAGE_URI"]

    DEFAULT_CONFIGURATION = {
        "version": "1.0.0",
        "logging": {
            "levels": {
                "console": "INFO",
                "logfile": "DEBUG"
            }
        }
    }


CONFIG_SETTINGS_ESTABLISHED = False

def establish_config_settings(*, name: Optional[str]=None, home_dir: Optional[str]=None,  settings_file: Optional[str]=None, extension_modules: Optional[str]=None, default_configuration: Optional[dict]=None, **other):

    global CONFIG_SETTINGS_ESTABLISHED

    if not CONFIG_SETTINGS_ESTABLISHED:
        CONFIG_SETTINGS_ESTABLISHED = True

        establish_presence_settings(name=name, home_dir=home_dir, settings_file=settings_file, extension_modules=extension_modules, **other)

        if default_configuration is not None:
            MOJO_CONFIG_DEFAULTS.DEFAULT_CONFIGURATION = default_configuration

    return