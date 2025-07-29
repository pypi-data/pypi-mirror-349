from enum import Enum
from pydantic import BaseModel, ConfigDict, Field


class CodeChallengeMethod(str, Enum):
    SHA256 = 'sha256'

class ResponseType(str, Enum):
    CODE = "code"

class GrantType(str, Enum):
    AUTHORIZATION_CODE = "authorization_code"
    REFRESH_TOKEN = "refresh_token"
    
class GenerateCodeVerifier(BaseModel):
    code_verifier: str
    code_challenge: str

class OAuthAuthorizationParam(BaseModel):
    client_id: str
    redirect_uri: str
    state: str
    code_challenge: str
    code_challenge_method: CodeChallengeMethod = Field(default=CodeChallengeMethod.SHA256)
    response_type: ResponseType = Field(default=ResponseType.CODE)

    model_config = ConfigDict(
        use_enum_values=True,
        validate_default=True
    )

class OAuthTokenParam(BaseModel):
    code_verifier: str
    client_id: str
    redirect_uri: str

class Token(BaseModel):
    application_id: str
    roles: list[str] = Field(default_factory=list)
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int
