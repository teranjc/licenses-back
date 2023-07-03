from fastapi import APIRouter, status, HTTPException, Depends, UploadFile, File, Form
from models.schemas import Users, ContainerModel
from repositories import ContainerRepository
from config.oauth import get_current_user

container_route = APIRouter()


@container_route.get("/containers", status_code=status.HTTP_200_OK)
async def get_license_with_container(current_user: Users = Depends(get_current_user)):
    try:
        return ContainerRepository.get_licenses_with_container()
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail={"status": e.status_code, "message": e.detail})


@container_route.post("/containers/detail", status_code=status.HTTP_200_OK)
async def get_license_with_container_detail(container_model: ContainerModel,
                           current_user: Users = Depends(get_current_user)):
    try:
        return ContainerRepository.get_container_license_detail(container_model)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail={"status": e.status_code, "message": e.detail})


@container_route.post("/containers", status_code=status.HTTP_200_OK)
async def create_container(container_model: ContainerModel,
                           current_user: Users = Depends(get_current_user)):
    try:
        return ContainerRepository.create_container(container_model)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail={"status": e.status_code, "message": e.detail})


@container_route.put("/containers", status_code=status.HTTP_200_OK)
async def update_license(container_model: ContainerModel,
                           current_user: Users = Depends(get_current_user)):
    try:
        return ContainerRepository.updated_container(container_model)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail={"status": e.status_code, "message": e.detail})


@container_route.post("/containers/check-connection", status_code=status.HTTP_200_OK)
async def check_connection(container_model: ContainerModel,
                           current_user: Users = Depends(get_current_user)):
    try:
        return ContainerRepository.verificar_conexion_ssh(container_model)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail={"status": e.status_code, "message": e.detail})

# @container_route.post("/containers", status_code=status.HTTP_200_OK)
# async def get_license_with_container(files: list[UploadFile] = File("files"), id_container: str = Form("idContainer"),
#                                      current_user: Users = Depends(get_current_user)):
#     try:
#         print(len(files))
#         print(id_container)
#     # return ContainerRepository.get_container_license_detail(container_model)
#     except HTTPException as e:
#         raise HTTPException(status_code=e.status_code, detail={"status": e.status_code, "message": e.detail})
