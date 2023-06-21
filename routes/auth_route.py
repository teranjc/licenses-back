from fastapi import APIRouter, status, HTTPException
from models.schemas import Login
from repositories import AuthRepository
auth_route = APIRouter()


@auth_route.post("/login", status_code=status.HTTP_200_OK)
async def login(user: Login):
    try:
        return AuthRepository.login(user)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail={"status": e.status_code, "message": e.detail})

