from fastapi import HTTPException, status
from pony.orm import db_session, select, desc, commit
from entities.license_managment import Users
from models.schemas import UsersList
from models.schemas import Users as UserModel
from config.utils import Hash


class UserRepository:
    def get_users():
        try:
            with db_session:

                list_users: list[UsersList] = []

                users = select(u for u in Users).order_by(desc(Users.id_user))

                for user in users:
                    list_users.append(UsersList(
                        id_user=user.id_user, name=user.name, last_name=user.last_name,
                        email=user.email, status=user.status
                    ))

                return {
                    "response": list_users
                }
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=f"{str(e.detail)}")

    def reset_password(user_model: UserModel):
        try:
            with db_session:

                user = select(u for u in Users if u.id_user == user_model.id_user).get()

                if user is None:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"El usuario con el id {user.id_user} no existe"
                    )

                user.password = Hash.has_password(user.email)
                print(user.email)
                commit()

                return {
                    "response": "Contraseña restablecida correctamente"
                }
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=f"{str(e.detail)}")
