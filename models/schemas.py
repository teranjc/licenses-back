from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Users(BaseModel):
    id_user: Optional[int]
    name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    password: Optional[str]
    status: Optional[int]


class UsersList(BaseModel):
    id_user: Optional[int]
    name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    status: Optional[int]

    def to_dict(self):
        return {
            'id_user': self.id_user,
            'name': self.name,
            'last_name': self.last_name,
            'email': self.email,
            'status': self.status
        }

    def __init__(self, id_user, name, last_name, email, status):
        super().__init__(
            id_user=id_user,
            name=name,
            last_name=last_name,
            email=email,
            status=status
        )


class Licenses(BaseModel):
    id_license: Optional[int]
    type: int
    fk_country_id: int
    name_unit: str
    key: str
    date_expiration: datetime
    date_created: Optional[datetime]
    status: Optional[int]

    def to_dict(self):
        return {
            'id_license': self.id_license,
            'type': self.type,
            'fk_country_id': self.fk_country_id,
            'name_unit': self.name_unit,
            'key': self.key,
            'date_expiration': self.date_expiration,
            'date_created': self.date_created,
            'status': self.status,
        }


class Login(BaseModel):
    email: str
    password: str
