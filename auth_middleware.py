from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone

# Configuración de los valores clave
SECRET_KEY = "Armenia2023@123"
ALGORITHM = "HS512"  # Asegúrate de que esto coincida con el algoritmo que usas para codificar
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Contexto de hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 esquema para manejar el token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Verificación de contraseña
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# Creación del token de acceso
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Dependencia para verificar el token
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    print ("pase por aqui")
    try:
        # Decodifica el token y verifica la clave secreta y el algoritmo
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            print("Username no encontrado en el token")  # Log para verificar problemas
            raise credentials_exception
    except JWTError as e:
        print(f"Error de JWT: {e}")  # Log para verificar problemas específicos de JWT
        raise credentials_exception
    return username




