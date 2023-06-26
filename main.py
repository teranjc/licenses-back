import asyncio
import json

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


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Configura la conexión SSH con los detalles del servidor remoto
    ssh.connect("192.168.100.160", port=4565, username='root', password='root')
    current_directory = '/'

    try:
        while True:
            data = await websocket.receive_text()
            if not data:
                break

            message = json.loads(data)
            print(data)
            command = message['command']
            directory = message['currentDirectory']
            print(directory)
            if directory:
                # Cambiar al directorio especificado
                command = f'cd {directory} && {command}'

            stdin, stdout, stderr = ssh.exec_command(command)
            output = stdout.read().decode('utf-8')
            error = stderr.read().decode('utf-8')

            if command.startswith('cd'):
                # Obtener el directorio actual después de cambiarlo
                stdin, stdout, stderr = ssh.exec_command('pwd')
                current_directory = stdout.read().decode('utf-8').strip()

            response = {
                'output': output,
                'error': error,
                'currentDirectory': current_directory
            }
            await websocket.send_text(json.dumps(response))

    finally:
        ssh.close()

load_dotenv()
app.include_router(auth_route, prefix="/api")
app.include_router(license_route, prefix="/api")
app.include_router(user_route, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
