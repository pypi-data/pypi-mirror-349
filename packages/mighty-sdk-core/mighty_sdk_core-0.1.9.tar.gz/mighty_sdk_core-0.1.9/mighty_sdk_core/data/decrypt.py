

from mighty_sdk_core.crypto.json_datagram import JSONDatagram
from mighty_sdk_core.crypto.symmetric_encryption import decrypt_symmetric
from mighty_sdk_core.data.types import EncryptedSharedData
from mighty_sdk_core.crypto.asymmetric_encryption import string_decrypt_asymmetric


SED_JSON_DATAGRAM = JSONDatagram("User Shared Encrypted Data Datagram")

def decrypt_shared_data(encrypted_data: EncryptedSharedData, public_key: str, private_key: str) -> str:
    """
    Decrypts the shared data using the provided public and private keys.

    Args:
        encrypted_data (EncryptedSharedData): The encrypted shared data to decrypt.
        public_key (str): The public key for decryption.
        private_key (str): The private key for decryption.

    Returns:
        str: The decrypted shared data.
    """
    
    data_key = string_decrypt_asymmetric(
        private_key,
        public_key,
        encrypted_data.public_key_encrypted_key
    )

    return decrypt_symmetric(
        message = encrypted_data.encrypted_data,
        symmetric_key = data_key,
        datagram = SED_JSON_DATAGRAM
    )
