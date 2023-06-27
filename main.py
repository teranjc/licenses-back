import asyncio
import json
import stat
from fastapi.responses import HTMLResponse
from fastapi import Request
from asyncssh import SSHServerSession
from fastapi import FastAPI, WebSocket
from dotenv import load_dotenv
import uvicorn
import paramiko
from starlette.middleware.cors import CORSMiddleware
from routes.auth_route import auth_route
from routes.license_route import license_route
from routes.user_route import user_route

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def index(request: Request):
    return HTMLResponse(open("index.html").read())


load_dotenv()
app.include_router(auth_route, prefix="/api")
app.include_router(license_route, prefix="/api")
app.include_router(user_route, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
