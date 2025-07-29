from enum import Enum

from pydantic import BaseModel

class ApplicationInformation(BaseModel):
    name: str
    description: str
    website: str
    is_active: bool
    permissions: list[str] # TODO: This type mighty change