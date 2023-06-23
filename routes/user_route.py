from fastapi import APIRouter, status, HTTPException, Depends
from repositories import UserRepository
from models.schemas import Users
from config.oauth import get_current_user
user_route = APIRouter()


@user_route.get("/users", status_code=status.HTTP_200_OK)
async def get_users(current_user: Users = Depends(get_current_user)):
    try:
        return UserRepository.get_users()
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail={"status": e.status_code, "message": e.detail})
