import datetime

from fastapi import HTTPException, status
from pony.orm import db_session, select, desc, commit
from models.schemas import Licenses as LicenseModel, LicensesDisabled
from entities.license_managment import Licenses, Countries, Users
from config.utils import Hash


class LicenseRepository:

    def get_licenses():
        try:
            with db_session:

                list_licenses = list()

                licenses = select(l for l in Licenses)
                for license in licenses:
                    list_licenses.append({
                        "id_license": license.id_license, "type": license.type,
                        "fk_country_id": license.fk_country_id.todict(),
                        "name_unit": license.name_unit,
                        "key": license.key,
                        "date_expiration": license.date_expiration,
                        "date_created": license.date_created,
                        "status": license.status
                    })

                return {
                    "response": list_licenses
                }
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=f"{str(e.detail)}")

    def create_licenses(license: LicenseModel):
        try:
            with db_session:
                licence_db = select(l for l in Licenses if l.key == license.key).get()
                if licence_db is None:
                    country = select(c for c in Countries if c.id_country == license.fk_country_id).get()

                    if country is None:
                        raise HTTPException(status_code=202, detail=f"El estado no se encuentra registrado"
                                            )

                    new_license = Licenses(type=license.type, fk_country_id=country,
                                           name_unit=license.name_unit, key=license.key,
                                           date_expiration=license.date_expiration,
                                           date_created=datetime.datetime.now(), status=1)

                    commit()
                else:
                    raise HTTPException(status_code=202, detail=f"La clave {license.key} ya se encuentra registrada"
                                        )
            return {
                "response": new_license.todict(),
                "status": 201
            }
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=f"{str(e.detail)}")

    def updated_licenses(license: LicenseModel):
        try:
            with db_session:
                licence_db = Licenses.get(id_license=license.id_license)
                if licence_db is None:
                    raise HTTPException(status_code=404, detail="La licencia no se encuentra registrada")

                # Actualizar los campos solo si se proporcionan en la solicitud
                if license.type is not None:
                    licence_db.type = license.type

                if license.fk_country_id is not None:
                    country = select(c for c in Countries if c.id_country == license.fk_country_id).get()
                    if country is None:
                        raise HTTPException(status_code=202, detail=f"El estado no se encuentra registrado"
                                            )
                    licence_db.fk_country_id = country

                if license.name_unit is not None:
                    licence_db.name_unit = license.name_unit

                if license.key is not None:
                    license_by_key = Licenses.get(lambda l: l.key == license.key and l.id_license != license.id_license)
                    if license_by_key is None:
                        licence_db.key = license.key
                    else:
                        raise HTTPException(status_code=404, detail="Esta clave ya se encuentra registrada")

                if license.date_expiration is not None:
                    # Validar que las fechas sean mayores.
                    licence_db.date_expiration = license.date_expiration

                commit()

                return {
                    "response": licence_db.todict()
                }

        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=f"{str(e.detail)}")

    def delete_licenses(license: LicensesDisabled, user: Users):
        try:
            with db_session:
                licence_db = select(l for l in Licenses if l.id_license == license.id_license).get()
                if licence_db is None:
                    raise HTTPException(status_code=404, detail="La licencia no se encuentra registrada")

                user_db = select(u for u in Users if user.id_user == u.id_user).get()
                if user_db is None:
                    raise HTTPException(status_code=404, detail="El usuario no esta registrado")

                if not Hash.verify_password(license.password, user_db.password):
                    raise HTTPException(
                        status_code=status.HTTP_202_ACCEPTED,
                        detail=f"La contraseña es incorrecta"
                    )
                # Actualizar los campos solo si se proporcionan en la solicitud
                # TODO realizar la conexion al contenedor y bajarlo

                licence_db.set(status=4)
                commit()
                return {
                    "response": "Licencia Eliminada correctamente"
                }

        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=f"{str(e.detail)}")

    def pause_license(license: LicensesDisabled, user: Users):
        try:
            with db_session:
                licence_db = select(l for l in Licenses if l.id_license == license.id_license).get()
                if licence_db is None:
                    raise HTTPException(status_code=404, detail="La licencia no se encuentra registrada")

                user_db = select(u for u in Users if user.id_user == u.id_user).get()
                if user_db is None:
                    raise HTTPException(status_code=404, detail="El usuario no esta registrado")

                if not Hash.verify_password(license.password, user_db.password):
                    raise HTTPException(
                        status_code=status.HTTP_202_ACCEPTED,
                        detail=f"La contraseña es incorrecta"
                    )
                # Actualizar los campos solo si se proporcionan en la solicitud
                # TODO realizar la conexion al contenedor y bajarlo
                licence_db.set(status=3)
                commit()
                return {
                    "response": "Licencia pausada correctamente"
                }

        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=f"{str(e.detail)}")

    def resume_license(license: LicensesDisabled, user: Users):
        try:
            with db_session:
                licence_db = select(l for l in Licenses if l.id_license == license.id_license).get()
                if licence_db is None:
                    raise HTTPException(status_code=404, detail="La licencia no se encuentra registrada")

                user_db = select(u for u in Users if user.id_user == u.id_user).get()
                if user_db is None:
                    raise HTTPException(status_code=404, detail="El usuario no esta registrado")

                if not Hash.verify_password(license.password, user_db.password):
                    raise HTTPException(
                        status_code=status.HTTP_202_ACCEPTED,
                        detail=f"La contraseña es incorrecta"
                    )
                # Actualizar los campos solo si se proporcionan en la solicitud
                # TODO realizar la conexion al contenedor y bajarlo
                license_by_key = Licenses.get(lambda l: l.key == license.key and l.id_license != license.id_license)
                if license_by_key is None:
                    licence_db.set(key=license.key)
                else:
                    raise HTTPException(status_code=404, detail="Esta clave ya se encuentra registrada")

                licence_db.set(date_expiration=license.date_expiration)
                licence_db.set(status=1)
                commit()
                return {
                    "response": "Licencia renovada correctamente"
                }

        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=f"{str(e.detail)}")
