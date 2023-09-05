"""
.. module:: cryptography
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module that contains cryptographic functions for working with encrypted
               configurations.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

import base64
import random

from cryptography.fernet import Fernet

from mojo.config.configurationformat import ConfigurationFormat

def encode_key(key: bytes) -> str:
    rtnval = base64.b64encode(key)
    return rtnval


def decode_key(encoded_key: str) -> bytes:
    rtnval = base64.b64decode(encoded_key)
    return rtnval


def generate_fernet_key(keyphrase: str) -> str:
    """
        Generates a 'Fernet' encryption and decryption key from the 'keyphrase' provided.

        :param keyphrase: The keyphrase to use to generate the encryption and decryption key.

        :returns: The generated encryption and decryption key
    """
    
    rgen = random.Random(keyphrase)

    key_bytes = rgen.randbytes(32)

    key = base64.urlsafe_b64encode(key_bytes)

    return key


def create_encrypted_configuration(key: str, plain_configuration: str, format: str=ConfigurationFormat.JSON):

    encrypted_configuration = encrypt_content(key, plain_configuration)

    docinfo = {
        "version": "1.0",
        "format": format,
        "encrypted_content": encrypted_configuration
    }

    return docinfo


def encrypt_content(key: str, plain_content: str) -> str:
    """
        Takes a plain content string and encrypts it with the key provided.  Then it
        converts the encrypted content to a base64 encoded str.
    """
    
    cryptor = Fernet(key)

    # Before we can encrypt the configuration content, we need to convert it to bytes
    plain_bytes = plain_content.encode("utf-8")

    # Encrypt the content with the key
    cypherbytes = cryptor.encrypt(plain_bytes)

    # Convert the cypher bytes to a base 64 str
    encrypted_content = base64.b64encode(cypherbytes).decode("utf-8")

    return encrypted_content


def decrypt_content(key: str, encrypted_content: str) -> str:
    """
        Takes a base64 encoded and encrypted content string and decodes the content into bytes.  Then
        it decrypts the content and encodes the result as a str
    """

    cryptor = Fernet(key)

    # Encrypted content is b64 encoded so decode it first into bytes
    cipherbytes = base64.b64decode(encrypted_content.encode("utf-8"))

    # Now we can decrypt the 
    plainbytes = cryptor.decrypt(cipherbytes)

    # Convert the plaing bytes to a str
    plaincontent = plainbytes.decode("utf-8")

    return plaincontent

