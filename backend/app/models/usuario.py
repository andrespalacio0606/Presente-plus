from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    activo = Column(Boolean, default=True)
    rol_id = Column(Integer, ForeignKey("rol.id"), nullable=False)

creado_en = Column(DateTime, default=datetime.utcnow)
actualizado_en = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

rol = relationship("Rol", backref="usuarios")
