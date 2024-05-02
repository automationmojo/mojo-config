
__author__ = "Myron Walker"
__copyright__ = "Copyright 2020, Myron W Walker"
__credits__ = []

from enum import Enum

class ConfigurationFormat(str, Enum):
    JSON = "json"
    YAML = "yaml"
