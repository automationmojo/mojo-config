"""
.. module:: overrides
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module that contains an enumeration of environment variable names
               that are used by the configuration code.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

class MOJO_CONFIG_OVERRIDES:

    MJR_NAME = "mjr"

    MJR_CONFIG_USE_CREDENTIALS = False
    MJR_CONFIG_USE_LANDSCAPE = False
    MJR_CONFIG_USE_RUNTIME = False
    MJR_CONFIG_USE_TOPOLOGY = False

    DEFAULT_CONFIGURATION = {
        "version": "1.0.0",
        "logging": {
            "levels": {
                "console": "INFO",
                "logfile": "DEBUG"
            }
        }
    }
