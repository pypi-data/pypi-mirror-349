
import os
from mighty_sdk_core.auth.oauth import get_user_info, get_user_info_biscuit
from mighty_sdk_core.data.decrypt import decrypt_shared_data
from mighty_sdk_core.mighty.client import MightyClient
from mighty_sdk_core.mighty.types import ApplicationInformation


class MightyApplicationClient(MightyClient):

    def __init__(self, api_key: str, app_private_key: str):
        self.api_key = api_key
        self.app_private_key = app_private_key

    def get_application_information(self) -> ApplicationInformation:
        pass

    async def get_user_data(self, token: str) -> str:
        """
        Fetches and decrypts user data using the provided token.

        Args:
            token (str): The token used for authentication.

        Returns:
            str: The decrypted user data.

        Raises:
            Exception: If there is an error during the fetching or decryption process.
        """
        # Get the user's shared encrypted data
        encrypted_data = await get_user_info(token, self.api_key)

        # Decrypt the shared data
        decrypted_data = decrypt_shared_data(encrypted_data, encrypted_data.associated_public_key, self.app_private_key)

        return decrypted_data
    
    async def get_user_data_biscuit(self, token: str) -> str:
        """
        Fetches and decrypts user data using the provided token.

        Args:
            token (str): The token used for authentication.

        Returns:
            str: The decrypted user data.

        Raises:
            Exception: If there is an error during the fetching or decryption process.
        """
        # Get the user's shared encrypted data
        encrypted_data = await get_user_info_biscuit(token, self.api_key)

        # Decrypt the shared data
        decrypted_data = decrypt_shared_data(encrypted_data, encrypted_data.associated_public_key, self.app_private_key)

        return decrypted_data