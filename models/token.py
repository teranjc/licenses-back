from typing import Optional

from jose import jwt,JWTError
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id_user: Optional[int] = None
    name: Optional[str] = None
    email: Optional[str] = None