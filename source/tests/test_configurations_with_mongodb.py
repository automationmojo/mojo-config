

import json
import os
import unittest


from mojo.config.configurationloader import ConfigurationLoader

TEST_MONGODB_HOSTNAME = "automation-mojo-db.q0jpg0g.mongodb.net"
TEST_MONGODB_DATABASE = "test-configuration"
TEST_MONGODB_COLLECTION = "credentials"

URI_ENCRYPTED_CONFIG = f"mongodb://{TEST_MONGODB_HOSTNAME}/{TEST_MONGODB_DATABASE}/{TEST_MONGODB_COLLECTION}"

TEST_MONGODB_DOCUMENT = "mojo-config-test-config-aaaa"

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


class TestMongoDBConfigEncryption(unittest.TestCase):

    
    def test_mongodb_config(self):

        if "AUTOMATION_MOJO_COUCHDB_PWD" not in os.environ:
            return

        mongodbuser = "datauser"
        mongodbpwd = os.environ["AUTOMATION_MOJO_MONGODB_PWD"].strip()

        credentials = {
            TEST_MONGODB_HOSTNAME: (mongodbuser, mongodbpwd)
        }

        config_uris =[
            URI_ENCRYPTED_CONFIG
        ]

        loader = ConfigurationLoader(config_uris, credentials=credentials)

        config_uri, config_info = loader.load_configuration(TEST_MONGODB_DOCUMENT, keyphrase="BlahBlah!!")

        return


if __name__ == '__main__':
    unittest.main()