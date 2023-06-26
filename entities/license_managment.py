from pony.orm import Required, Optional, PrimaryKey, Set, perm
from config import db
from datetime import datetime


class Users(db.Entity):
    id_user = PrimaryKey(int, auto=True)
    name = Required(str, 50)
    last_name = Required(str, 50)
    email = Required(str, 50)
    password = Required(str, 250)
    status = Required(int)


class Countries(db.Entity):
    id_country = PrimaryKey(int, auto=True)
    name = Required(str)
    licenses = Set('Licenses')

    def todict(self):
        return {
            'id_country': self.id_country,
            'name': self.name
        }


class Licenses(db.Entity):
    id_license = PrimaryKey(int, auto=True)
    type = Required(int)
    fk_country_id = Required(Countries)
    name_unit = Required(str)
    key = Required(str, unique=True)
    date_expiration = Required(datetime)
    date_created = Required(datetime)
    status = Required(int)
    is_redeemed = Required(bool)

    def todict(self):
        return {
            'id_license': self.id_license,
            'type': self.type,
            'fk_country_id': self.fk_country_id.todict(),
            'name_unit': self.name_unit,
            'key': self.key,
            'date_expiration': self.date_expiration.strftime('%Y-%m-%d %H:%M:%S'),
            'date_created': self.date_created.strftime('%Y-%m-%d %H:%M:%S'),
            'status': self.status
        }


db.generate_mapping(create_tables=True, check_tables=True)
