import os
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from semver_range import Version
from .aad_meta import AADMeta
from .json_datagram import JSONDatagram
from .utils import concat_uint8_arrays

NONCE_LENGTH = 12

class TaggedSecretBox:
    """
    A class to handle encryption and decryption using the ChaCha20Poly1305 algorithm
    with additional authenticated data (AAD) metadata.

    Attributes:
        key (ChaCha20Poly1305): The encryption key.
    """
    def __init__(self, key_bytes: bytes) -> None:
        """
        Initialize a TaggedSecretBox instance.

        :param key_bytes: The encryption key as bytes.
        """
        self.key = ChaCha20Poly1305(key_bytes)

    def encrypt(self, datagram: JSONDatagram, data: str, nonce = os.urandom(NONCE_LENGTH)) -> bytearray:
        """
        Encrypt the given data using the provided JSON datagram and nonce.

        :param datagram: The JSONDatagram object containing metadata for encryption.
        :param data: The plaintext data to be encrypted.
        :param nonce: The nonce to be used for encryption. Defaults to a random nonce.
        :return: The encrypted data as a bytearray.
        """
        aad = AADMeta(datagram.version, datagram.type, nonce)
        aad_serialized = aad.serialize()

        return concat_uint8_arrays(aad_serialized, self.key.encrypt(nonce, datagram.serialize(data), aad_serialized))

    def decrypt(self, datagram: JSONDatagram, bytes: bytes) -> str:
        """
        Decrypt the given byte array using the provided JSON datagram.

        :param datagram: The JSONDatagram object containing metadata for decryption.
        :param bytes: The encrypted data as a byte array.
        :return: The decrypted data as a string.
        :raises Exception: If decryption fails due to invalid key, type mismatch, or version constraint violation.
        """
        header = AADMeta.deserialize(bytes)
        if header is None or "metadata" not in header.keys():
            raise Exception("Couldn't decrypt: no header in provided data")
        
        decrypted = self.key.decrypt(header["metadata"].nonce, header["content"], header["raw_metadata"])

        if decrypted is None:
            raise Exception("Couldn't decrypt: invalid key")

        if datagram.type != header["metadata"].type:
            raise Exception("Couldn't decrypt: encrypted type ({}) doesn't match datagram type ({})".format(header["metadata"].type, datagram.type))

        if not (Version(header["metadata"].version) in datagram.version_constraint):
            raise Exception("Couldn't decrypt: encrypted version ({}) doesn't match datagram version constraint ({})".format(header["metadata"].version, datagram.version_constraint))

        return datagram.deserialize(decrypted)