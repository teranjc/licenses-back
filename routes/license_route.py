from fastapi import APIRouter, status, HTTPException, Depends
from repositories.license_repository import LicenseRepository
from models.schemas import Users, Licenses as LicenseModel
from config.oauth import get_current_user

license_route = APIRouter()


@license_route.get("/licenses", status_code=status.HTTP_200_OK)
async def get_licenses(current_user: Users = Depends(get_current_user)):
    try:
        return LicenseRepository.get_licenses()
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail={"status": e.status_code, "message": e.detail})


@license_route.post("/licenses", status_code=status.HTTP_201_CREATED)
async def create_licenses(model: LicenseModel, current_user: Users = Depends(get_current_user), ):
    try:
        return LicenseRepository.create_licenses(model)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail={"status": e.status_code, "message": e.detail})

@license_route.put("/licenses", status_code=status.HTTP_200_OK)
async def updated_licenses(model: LicenseModel, current_user: Users = Depends(get_current_user), ):
    try:
        return LicenseRepository.updated_licenses(model)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail={"status": e.status_code, "message": e.detail})
