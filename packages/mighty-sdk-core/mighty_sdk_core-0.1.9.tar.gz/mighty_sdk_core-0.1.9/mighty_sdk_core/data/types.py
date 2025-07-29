from pydantic import BaseModel

class EncryptedSharedData(BaseModel):
    encrypted_data: str
    public_key_encrypted_key: str
    associated_public_key: str

