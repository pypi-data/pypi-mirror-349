import os
import aiohttp
from mighty_sdk_core.data.types import EncryptedSharedData
from mighty_sdk_core.data.decrypt import decrypt_shared_data
from mighty_sdk_core.mighty.client import MightyClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"))

mighty_base_url = os.getenv("MIGHTY_BASE_URL", "http://localhost:8080")
user_data_url = f"{mighty_base_url}/api/v1/encrypted-data"

"""
MightyUserDataClient is a client for fetching and decrypting user data from the Mighty Network API.

Attributes:
    api_key (str): The API key for accessing the Mighty Network API.
    api_public_key (str): The public key for decrypting the data.
    api_private_key (str): The private key for decrypting the data.
    data_url (str): The URL endpoint for fetching the encrypted data.

Methods:
    get_data() -> str:
        Asynchronously fetches and decrypts the user data from the API.
"""
class MightyUserDataClient(MightyClient):
    api_key: str
    api_public_key: str
    api_private_key: str

    def __init__(self, api_key: str, api_public_key: str, api_private_key: str):
        super().__init__()
        self.api_key = api_key
        self.api_public_key = api_public_key
        self.api_private_key = api_private_key

    async def get_data(self) -> str:
        try:
            encrypted_data = await self._get_data_by_api_key(self.api_key, user_data_url)
            decrypted_data = decrypt_shared_data(encrypted_data, self.api_public_key, self.api_private_key)

            return decrypted_data
        except Exception as e:
            raise e

    async def _get_data_by_api_key(self, api_key: str, data_url: str) -> EncryptedSharedData:
        async with aiohttp.ClientSession() as session:
            headers = {
                "x-api-key": api_key,
                "User-Agent": "Mozilla/5.0"
            }
            async with session.get(data_url, headers=headers) as response:
                return EncryptedSharedData(**await response.json())