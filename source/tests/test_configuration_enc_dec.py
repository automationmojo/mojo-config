

import json
import unittest


from mojo.config.cryptography import (
    create_encrypted_configuration,
    decrypt_content,
    generate_fernet_key
)

CREDENTIAL_CONTENT = """
credentials:
    -   identifier: adminuser
        category:
            - basic
            - ssh
        username: adminuser
        password: "something"
    
    -   identifier: datauser
        category: basic
        username: datauser
        password: "something"

    -   identifier: pi-cluster
        category: ssh
        username: pi
        password: "something"
        primitive: True
"""

class TestConfigurationEncryption(unittest.TestCase):
    
    def test_encrypted_configuration_creation(self):

        key = generate_fernet_key("BlahBlah!!")

        econf_info = create_encrypted_configuration(key, CREDENTIAL_CONTENT)

        cipher_content = econf_info["encrypted_content"]

        econf_doc_content = json.dumps(econf_info, indent=4)

        plain_content = decrypt_content(key, cipher_content)

        return

if __name__ == '__main__':
    unittest.main()
