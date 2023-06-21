from fastapi import HTTPException
from pony.orm import db_session, select, desc
from entities.license_managment import Users
from models.schemas import UsersList


class UserRepository:
    def get_users():
        try:
            with db_session:

                list_users: list[UsersList] = []

                users = select(u for u in Users).order_by(desc(Users.id_user))

                for user in users:
                    list_users.append(UsersList(
                        id_user=user.id_user,name=user.name,last_name=user.last_name,
                        email=user.email,status=user.status
                    ))


                return {
                    "response": list_users
                }
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=f"{str(e.detail)}")
