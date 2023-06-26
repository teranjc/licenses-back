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


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    # Crear instancia de SSHClient
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Conectar al servidor SSH
    client.connect("192.168.100.160", port=4565, username='root', password='root')
    # Crear instancia de SFTPClient
    sftp = client.open_sftp()

    # Directorio actual
    current_directory = "/"

    try:
        while True:
            # Leer el comando del cliente WebSocket
            command = await websocket.receive_text()

            if command.lower() == "exit":
                # Salir del bucle si se ingresa "exit"
                break

            if command.lower().startswith("cd"):
                # Cambiar de directorio
                _, path = command.split(" ", 1)
                if path == "..":
                    # Retroceder un nivel
                    current_directory = "/".join(current_directory.split("/")[:-1])
                elif path.startswith("/"):
                    # Directorio absoluto
                    try:
                        attributes = sftp.lstat(path)
                        if stat.S_ISDIR(attributes.st_mode):
                            current_directory = path
                            await websocket.send_text(current_directory)  # Enviar la ruta del directorio actual
                        else:
                            await websocket.send_text(f"{path} no es un directorio válido.")
                    except FileNotFoundError:
                        await websocket.send_text(f"{path} no existe.")
                    except Exception as e:
                        await websocket.send_text(f"Error al verificar el directorio: {e}")
                else:
                    # Directorio relativo
                    path = current_directory + "/" + path
                    try:
                        attributes = sftp.lstat(path)
                        if stat.S_ISDIR(attributes.st_mode):
                            current_directory = path
                            await websocket.send_text(current_directory)  # Enviar la ruta del directorio actual
                        else:
                            await websocket.send_text(f"{path} no es un directorio válido.")
                    except FileNotFoundError:
                        await websocket.send_text(f"{path} no existe.")
                    except Exception as e:
                        await websocket.send_text(f"Error al verificar el directorio: {e}")
            else:
                # Ejecutar el comando en la terminal remota
                stdin, stdout, stderr = client.exec_command(f"cd {current_directory}; {command}")

                # Leer la salida del comando
                output = stdout.read().decode('utf-8')
                error = stderr.read().decode('utf-8')

                if output:
                    await websocket.send_text(output)

                if error:
                    await websocket.send_text(error)

                # Enviar la ruta del directorio actual después de ejecutar el comando
                await websocket.send_text(current_directory)

    finally:
        # Cerrar la conexión SSH y SFTP
        sftp.close()
        client.close()


@app.get("/")
async def index(request: Request):
    return HTMLResponse(open("index.html").read())


load_dotenv()
app.include_router(auth_route, prefix="/api")
app.include_router(license_route, prefix="/api")
app.include_router(user_route, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
