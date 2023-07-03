from fastapi import HTTPException
from entities.license_managment import Container, Licenses
from pony.orm import *
from models.schemas import ContainerModel
import paramiko


class ContainerRepository:

    def get_licenses_with_container():
        try:
            with db_session:

                list_containers = list()

                containers = select(c for c in Container)
                license_with_containers = left_join((c, l) for c in Container for l in c.fk_license_id)
                license_with_containers_1 = left_join((l, c) for l in Licenses for c in l.containers)
                # for cont in containers:
                #     list_containers.append({
                #         "id_container": cont.id_container, "ip": cont.ip,
                #         "project": cont.project,
                #         "user": cont.user,
                #         "port": cont.port,
                #         "path": cont.path,
                #         "license": cont.fk_license_id.todict(),
                #     })
                for lic, container in license_with_containers_1:
                    list_containers.append({
                        "id_licence": lic.id_license,
                        "key": lic.key,
                        "type": lic.type,
                        "name_unit": lic.name_unit,
                        "date_expiration": lic.date_expiration,
                        "country": lic.fk_country_id.name,
                        "date_created": lic.date_created,
                        "is_redeemed": lic.is_redeemed,
                        "has_container": False if container is None else True,
                        "status":lic.status,
                        "container": None if container is None else container.todict_without_license(),
                    })

                return {
                    "response": list_containers
                }
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=f"{str(e.detail)}")

    def get_container_license_detail(container_model: ContainerModel):
        try:
            with db_session:
                container = select(c for c in Container if container_model.id_container == c.id_container).get()
                if container is None:
                    raise HTTPException(
                        status_code=404,
                        detail="No exite ningun contenedor con ese id"
                    )
                return {
                    "response": container.todict()
                }
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=f"{str(e.detail)}")

    def create_container(container_model: ContainerModel):
        try:
            with db_session:
                license = select(l for l in Licenses if l.id_license == container_model.license).get()
                if license is None:
                    raise HTTPException(status_code=404, detail="La licencia no se encuentra registrada")

                container = select(c for c in Container if container_model.license == license).get()
                if container is not None:
                    raise HTTPException(status_code=202, detail="Ya existe un contenedor con esa licencia")

                new_container = Container(
                    id_container=container_model.id_container,
                    ip=container_model.ip, user=container_model.user,
                    password=container_model.password,
                    port=container_model.port,
                    fk_license_id=license,
                    project=container_model.project,
                    path=container_model.path
                )

                commit()
                return {
                    "response": new_container.todict()
                }
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=f"{str(e.detail)}")

    def updated_container(container_model: ContainerModel):
        try:
            with db_session:

                container_db = select(c for c in Container if container_model.id_container == c.id_container).get()
                if container_db is None:
                    raise HTTPException(status_code=404, detail="El contenedor no existe")

                license = select(l for l in Licenses if l.id_license == container_model.license).get()
                if license is None:
                    raise HTTPException(status_code=404, detail="La licencia no se encuentra registrada")

                container = Container.get(lambda
                                              c: c.fk_license_id == license and c.id_container != container_model.id_container)
                if container is not None:
                    raise HTTPException(status_code=202, detail="Ya existe un contenedor con esa licencia")

                container_db.ip = container_model.ip or container_db.ip
                container_db.user = container_model.user or container_db.user
                container_db.password = container_model.password or container_db.password
                container_db.port = container_model.port or container_db.port
                container_db.path = container_model.path or container_db.path
                container_db.project = container_model.project or container_db.project
                container_db.fk_license_id = license or container_db.fk_license_id

                commit()
                return {
                    "response": container_db.todict()
                }
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=f"{str(e.detail)}")

    def verificar_conexion_ssh(container_model: ContainerModel):
        host = container_model.ip
        username = container_model.user
        password = container_model.password
        port = container_model.port
        ssh = paramiko.SSHClient()
        try:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, port=port, username=username, password=password)
            return {
                "response": "Conexión SSH exitosa",
                "code": 200
            }
        except paramiko.AuthenticationException:
            raise HTTPException(status_code=400,
                                detail="Error de autenticación. Verifica las credenciales de conexión.")
        except paramiko.SSHException as ssh_exc:
            raise HTTPException(status_code=400, detail=f"Error en la conexión SSH: {str(ssh_exc)}")
        except paramiko.ssh_exception.NoValidConnectionsError:
            raise HTTPException(status_code=400,
                                detail="No se pudo establecer una conexión SSH. Verifica la dirección IP y la disponibilidad del servidor.")

        except Exception as e:
            raise HTTPException(status_code=400,
                                detail=f"Error inesperado: {str(e)}")
        finally:
            ssh.close()

    # Parámetros de conexión SSH
