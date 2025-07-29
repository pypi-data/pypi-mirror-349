import base64
from .tagged_secret_box import *

def raw_encrypt_symmetric(content: str, symmetric_key: str, datagram: JSONDatagram):
    """
    Encrypts the given content using a symmetric key and a JSON datagram.

    :param content: The plaintext content to be encrypted.
    :param symmetric_key: The base64 encoded symmetric key for encryption.
    :param datagram: The JSONDatagram object containing metadata for encryption.
    :return: The encrypted content as a byte array.
    """
    secret_box = TaggedSecretBox(base64.b64decode(symmetric_key))
    return secret_box.encrypt(datagram, content)

def encrypt_symmetric(content: str, symmetric_key: str, datagram: JSONDatagram):
    """
    Encrypts the given content using a symmetric key and a JSON datagram, then encodes the result in base64.

    :param content: The plaintext content to be encrypted.
    :param symmetric_key: The base64 encoded symmetric key for encryption.
    :param datagram: The JSONDatagram object containing metadata for encryption.
    :return: The encrypted content as a base64 encoded byte array.
    """
    return base64.b64encode(raw_encrypt_symmetric(content, symmetric_key, datagram))

def raw_decrypt_symmetric(message: bytes, symmetric_key: str, datagram: JSONDatagram):
    """
    Decrypts the given encrypted message using a symmetric key and a JSON datagram.

    :param message: The encrypted message as a byte array.
    :param symmetric_key: The base64 encoded symmetric key for decryption.
    :param datagram: The JSONDatagram object containing metadata for decryption.
    :return: The decrypted content as a string.
    """
    secret_box = TaggedSecretBox(base64.b64decode(symmetric_key))
    return secret_box.decrypt(datagram, message)

def decrypt_symmetric(message: str, symmetric_key: str, datagram: JSONDatagram):
    """
    Decrypts the given base64 encoded encrypted message using a symmetric key and a JSON datagram.

    :param message: The encrypted message as a base64 encoded string.
    :param symmetric_key: The base64 encoded symmetric key for decryption.
    :param datagram: The JSONDatagram object containing metadata for decryption.
    :return: The decrypted content as a string.
    """
    return raw_decrypt_symmetric(base64.b64decode(message), symmetric_key, datagram)
