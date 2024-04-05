
import unittest

from mojo.config.sources.httpsource import HttpSource

class TestCouchDBConfigEncryption(unittest.TestCase):

    
    def test_http_parse(self):

        source = HttpSource.parse("http://somehost.com/someleaf/")

        assert source != None, "The returned source for an 'http' uri should not have been None"

        return

    def test_https_parse(self):

        source = HttpSource.parse("https://somehost.com/someleaf/")

        assert source != None, "The returned source for an 'https' uri should not have been None"

        return



if __name__ == '__main__':
    unittest.main()