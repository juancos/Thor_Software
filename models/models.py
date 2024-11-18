from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    team = Column(String)  # Ejemplo: 'ventas', 'marketing', 'logistica'
    role = Column(String)  # Ejemplo: 'admin', 'usuario'
