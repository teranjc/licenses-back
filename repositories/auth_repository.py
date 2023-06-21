from fastapi import HTTPException, status
from models.schemas import Login
from pony.orm import db_session, commit, select, desc
from entities.license_managment import Users
from config.utils import Hash
from datetime import timedelta
from config.token import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token


class AuthRepository:
    def login(user: Login):
        try:
            with db_session:
                userDb = Users.get(email=user.email)
                if not userDb:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                        "message": "User not found"
                    })
                if not Hash.verify_password(user.password, userDb.password):
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Usuario y/o contraseña son incorrectos."
                    )
                access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
                access_token = create_access_token(
                    data={"sub": userDb.name + " " + userDb.last_name, "email": userDb.email, "id": userDb.id_user},
                    expires_delta=access_token_expires
                )

                return {"access_token": access_token, "token_type": "bearer"}
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=f"{str(e.detail)}")
