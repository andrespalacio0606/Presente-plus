from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Participante(Base):
    __tablename__ = "participante"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    dni = Column(String(20), unique=True, nullable=False)
    fecha_nacimiento = Column(Date)
    domicilio = Column(String(100))
    telefono = Column(String(20))
    estado = Column(String(20), default="activo")

    creado_en = Column(DateTime, default=datetime.utcnow)
    actualizado_en = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    usuario = relationship("usuario", backref="participantes")
    tutores = relationship("Tutor", backref="participante")
    asistencias = relationship("Asistencia", backref="participante")
    alertas = relationship("Alerta", backref="participante")
