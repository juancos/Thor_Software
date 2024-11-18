from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import User
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta, timezone
from auth_middleware import create_access_token, oauth2_scheme, get_password_hash, verify_password,  get_current_user

# Inicializa el router de FastAPI
router = APIRouter()

# Clave secreta para JWT
SECRET_KEY = "Armenia2023@123"
ALGORITHM = "HS512"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Modelo de solicitud para el registro
class UserCreate(BaseModel):
    username: str
    password: str

# Modelo de respuesta para el token
class Token(BaseModel):
    access_token: str
    token_type: str

# Dependencia para la sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint para registrar usuarios
@router.post("/register", response_model=UserCreate)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Endpoint para iniciar sesión y obtener un token JWT
@router.post("/login", response_model=Token)
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}


# Endpoint protegido que requiere un token de acceso
@router.get("/protected")
async def read_protected_data(token: str = Depends(get_current_user)):
    print ("pase por aqui")

    #await get_current_user("") 
    return {"message": "Tienes acceso al contenido protegido"}

    return {"message": "Tienes acceso al contenido protegido"}
