from datetime import timedelta, datetime
from typing import Optional

from jose import jwt, JWTError

from models.token import TokenData

SECRET_KEY = "3r1774n"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 42000


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        name: str = payload.get("sub")
        id_user: str = payload.get("id")
        email: str = payload.get("email")
        if name is None:
            raise credentials_exception
        token_data = TokenData(id_user=id_user, name=name, email=email)
        print(token_data)
    except JWTError:
        raise credentials_exception
    return token_data
