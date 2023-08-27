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

class MOJO_CONFIG_OVERRIDES:

    MJR_NAME = "mjr"

    MJR_HOME_DIRECTORY = os.path.expanduser("~/{}".format(MJR_NAME))

    MJR_CONFIG_REQUIRE_CREDENTIALS = False
    MJR_CONFIG_REQUIRE_LANDSCAPE = False
    MJR_CONFIG_REQUIRE_RUNTIME = False
    MJR_CONFIG_REQUIRE_TOPOLOGY = False

    DEFAULT_CONFIGURATION = {
        "version": "1.0.0",
        "logging": {
            "levels": {
                "console": "INFO",
                "logfile": "DEBUG"
            }
        }
    }
