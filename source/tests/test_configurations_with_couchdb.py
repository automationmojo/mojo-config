

import os
import unittest


from mojo.config.configurationloader import ConfigurationLoader

TEST_COUCHDB_HOSTNAME = "couchdb.automationmojo.com"
TEST_COUCHDB_DATABASE = "test-mojo-config"

URI_ENCRYPTED_CONFIG = f"couchdb://https+{TEST_COUCHDB_HOSTNAME}/{TEST_COUCHDB_DATABASE}"

TEST_COUCHDB_DOCUMENT = "mojo-config-test-config-aaaa"

CREDENTIAL_CONTENT = {
    "credentials": [
        {
            "identifier": "adminuser",
            "category": [
                "basic",
                "ssh"
            ],
            "username": "adminuser",
            "password": "something"
        },
        {
            "identifier": "datauser",
            "category": "basic",
            "username": "datauser",
            "password": "something"
        },
        {
            "identifier": "pi-cluster",
            "category": "ssh",
            "username": "pi",
            "password": "something",
            "primitive": True
        }
    ]
}


class TestCouchDBConfigEncryption(unittest.TestCase):

    
    def test_couchdb_config(self):

        assert "AUTOMATION_MOJO_COUCHDB_PWD" in os.environ, "The 'AUTOMATION_MOJO_COUCHDB_PWD' environment variable must be set for running tests."

        couchdbuser = "datauser"
        couchdbpwd = os.environ["AUTOMATION_MOJO_COUCHDB_PWD"].strip()

        credentials = {
            TEST_COUCHDB_HOSTNAME: (couchdbuser, couchdbpwd)
        }

        config_uris =[
            URI_ENCRYPTED_CONFIG
        ]

        loader = ConfigurationLoader(config_uris, credentials=credentials)

        config_uri, config_info = loader.load_configuration_by_name(TEST_COUCHDB_DOCUMENT, keyphrase="BlahBlah!!")

        return


if __name__ == '__main__':
    unittest.main()