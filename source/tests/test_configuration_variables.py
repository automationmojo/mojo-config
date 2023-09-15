
import os

import unittest


from mojo.config.normalize import (
    split_and_normalize_source_list
)

class TestConfigurationEncryption(unittest.TestCase):
    
    def test_split_search_paths_with_one_path(self):
        search_paths = "~/config/landscapes"

        paths = split_and_normalize_source_list(search_paths)
        self.assert_(len(paths) == 1, "The length of the paths found should have been 1.")
        return

    def test_split_search_paths_with_one_path(self):
        search_paths = "~/config/landscapes;~/other/path"

        paths = split_and_normalize_source_list(search_paths)
        self.assert_(len(paths) == 2, "The length of the paths found should have been 1.")
        return

if __name__ == '__main__':
    unittest.main()
