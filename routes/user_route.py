from fastapi import APIRouter, status, HTTPException
from repositories import UserRepository
user_route = APIRouter()


@user_route.get("/users", status_code=status.HTTP_200_OK)
async def get_users():
    try:
        return UserRepository.get_users()
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail={"status": e.status_code, "message": e.detail})
