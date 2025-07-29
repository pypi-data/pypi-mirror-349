from base64 import urlsafe_b64encode
from hashlib import sha256
from json import dumps
import os
import aiohttp
from mighty_sdk_core.auth.secret import random_secret
from mighty_sdk_core.auth.types import GenerateCodeVerifier, GrantType, OAuthAuthorizationParam, OAuthTokenParam, Token, BiscuitToken
import urllib
from dotenv import load_dotenv

from mighty_sdk_core.data.types import EncryptedSharedData


API_KEY_HEADER = "x-api-key"
BISCUIT_HEADER = "x-biscuit"
AUTHORIZATION_HEADER = "Authorization"
SECRET_LENGTH = 128

base_headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0"
}

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"))

mighty_base_url = os.getenv("MIGHTY_BASE_URL", "http://localhost:8080")
authorize_url = f"{mighty_base_url}/mighty-oauth/authorization"
token_url = f"{mighty_base_url}/mighty-oauth/token"
refresh_token_url = f"{mighty_base_url}/mighty-oauth/refresh-token"
user_info_url = f"{mighty_base_url}/api/v1/app/user-data"
user_info_url_biscuit = f"{mighty_base_url}/api/v1/app/biscuit/user-data"
biscuit_token_url = f"{mighty_base_url}/mighty-oauth/biscuit-token"

def generate_code_verifier() -> GenerateCodeVerifier:
    """
    Generates a code verifier for the OAuth2 authorization process.

    A code verifier is a cryptographically random string that is used to
    mitigate authorization code interception attacks. It is part of the
    Proof Key for Code Exchange (PKCE) extension to OAuth2.

    Returns:
        str: The generated code verifier.
    """
    # Random the code verifier
    # Reference: https://aaronparecki.com/oauth-2-simplified/#:~:text=(ietf.org).-,Authorization,-Create%20a%20random
    code_verifier = random_secret(SECRET_LENGTH)

    # Hash and encode the code verifier
    bin_code_verifier = sha256(code_verifier.encode('utf-8')).digest()
    code_challenge = urlsafe_b64encode(bin_code_verifier).decode("utf-8").replace("=", "")

    return GenerateCodeVerifier(code_verifier=code_verifier, code_challenge=code_challenge)

def get_authorization_url(oauth_config: OAuthAuthorizationParam) -> str:
    """
    Builds the authorization URL for the application.

    This method constructs the URL that can be used to authorize the application
    with the necessary permissions and access rights.

    Returns:
        str: The constructed authorization URL.
    """

    params = urllib.parse.urlencode(oauth_config.model_dump())
    return f"{authorize_url}?{params}"

async def exchange_code_for_token(code: str, application_api_key: str, oauth_config: OAuthTokenParam) -> Token:
    """
    Exchanges an authorization code for an access token.

    This method sends the authorization code to the token endpoint to obtain an access token.

    Args:
        code (str): The authorization code to exchange for an access token.
        application_api_key (str): The API key of the application.

    Returns:
        Token: The access token and associated information.
    """

    async with aiohttp.ClientSession() as session:
        headers = {
            **base_headers,
            API_KEY_HEADER: application_api_key
        }
        payload = {
            "code": code,
            "grant_type": GrantType.AUTHORIZATION_CODE.value,
            "code_verifier": oauth_config.code_verifier,
            "redirect_uri": oauth_config.redirect_uri,
            "client_id": oauth_config.client_id
        }
        async with session.post(token_url, data=dumps(payload), headers=headers) as response:
            try:
                response_json = await response.json()
                response_json["application_id"] = response_json.pop("username", None)
                return Token(**response_json)
            except Exception as e:
                raise Exception(f"Failed to exchange code for token: {e}")

async def get_user_info(token: str, application_api_key: str) -> EncryptedSharedData:
    """
    Retrieves user information from the Mighty API.

    This method sends a request to the user info endpoint with the provided access token
    to retrieve user-specific data.
    """
    async with aiohttp.ClientSession() as session:
        headers = {
            **base_headers,
            AUTHORIZATION_HEADER: f"Bearer {token}",
            API_KEY_HEADER: application_api_key
        }
        async with session.get(user_info_url, headers=headers) as response:
            try:
                return EncryptedSharedData(**await response.json())
            except Exception as e:
                raise Exception(f"Failed to get user info: {e}. Please verify that the application has invited you and that your access token is valid. Refer to the Mighty Network API documentation at docs.mightynetwork.ai for further guidance.")

async def exchange_code_for_biscuit_token(code: str, expiration: int, usage_once: bool, application_api_key: str, oauth_config: OAuthTokenParam) -> BiscuitToken:
    """
    Exchanges an authorization code for an access token.
    This method sends the authorization code to the token endpoint to obtain an access token.
    Args:
        code (str): The authorization code to exchange for an access token.
        application_api_key (str): The API key of the application.
    Returns:
        Token: The access token and associated information.
    """
    async with aiohttp.ClientSession() as session:
        headers = {
            **base_headers,
            API_KEY_HEADER: application_api_key
        }
        payload = {
            "code": code,
            "grant_type": GrantType.AUTHORIZATION_CODE.value,
            "code_verifier": oauth_config.code_verifier,
            "redirect_uri": oauth_config.redirect_uri,
            "client_id": oauth_config.client_id,
            "expiration": expiration,
            "usage_once": usage_once
        }
        async with session.post(biscuit_token_url, data=dumps(payload), headers=headers) as response:
            try:
                response_json = await response.json()
                return BiscuitToken(**response_json)
            except Exception as e:
                raise Exception(f"Failed to exchange code for token: {e}")
            
async def get_user_info_biscuit(biscuit: str, application_api_key: str) -> EncryptedSharedData:
    """
    Retrieves user information from the Mighty API.
    This method sends a request to the user info endpoint with the provided access token
    to retrieve user-specific data.
    """
    async with aiohttp.ClientSession() as session:
        headers = {
            **base_headers,
            BISCUIT_HEADER: biscuit,
            API_KEY_HEADER: application_api_key
        }
        async with session.get(user_info_url_biscuit, headers=headers) as response:
            try:
                return EncryptedSharedData(**await response.json())
            except Exception as e:
                raise Exception(f"Failed to get user info: {e}. Please verify that the application has invited you and that your access token is valid. Refer to the Mighty Network API documentation at docs.mightynetwork.ai for further guidance.")

async def refresh_token(refresh_token: str, application_api_key: str) -> Token:
    """
    Refreshes an access token using a refresh token.

    This method sends a request to the token endpoint with the provided refresh token
    to obtain a new access token.
    """
    async with aiohttp.ClientSession() as session:
        headers = {
            **base_headers,
            API_KEY_HEADER: application_api_key
        }
        payload = {
            "grant_type": GrantType.REFRESH_TOKEN.value,
            "refresh_token": refresh_token
        }
        async with session.post(refresh_token_url, data=dumps(payload), headers=headers) as response:
            try:
                response_json = await response.json()
                response_json["application_id"] = response_json.pop("username", None)
                return Token(**response_json)
            except Exception as e:
                raise Exception(f"Failed to refresh token: {e}")
