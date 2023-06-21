from fastapi import  HTTPException, status

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from config.token import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={
            "message": "Token invalido"
        },
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_token(token, credentials_exception)
