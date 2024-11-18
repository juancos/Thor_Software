# -*- coding: utf-8 -*-
from fastapi import FastAPI, Depends
from Routes.auth_routes import router as auth_router  # Importa el router de auth_routes
from auth_middleware import oauth2_scheme, create_access_token, get_current_user
from pydantic import BaseModel

app = FastAPI()

# Incluir las rutas de autenticación
app.include_router(auth_router)

# Modelo de datos para la solicitud de generación de token
class TokenRequest(BaseModel):
    username: str
    password: str

# Endpoint raíz
@app.get("/")
async def root():
    return {"message": "¡Hola, Thor Software está listo!"}

# Endpoint para generar un token de acceso
@app.post("/token")
async def generate_token(request: TokenRequest):
    # Validar las credenciales y generar el token
    token = create_access_token(data={"sub": request.username})
    return {"access_token": token, "token_type": "bearer"}

# Endpoint protegido que requiere un token de acceso
@app.get("/protected")
async def read_protected_data(current_user: str = Depends(get_current_user)):
    print ("pase por aqui")
    raise Exception("")
    get_current_user("")
    return {"message": "Tienes acceso al contenido protegido"}







