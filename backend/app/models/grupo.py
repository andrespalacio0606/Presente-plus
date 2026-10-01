from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

participante_grupo = Table(
    "participante_grupo",
    Base.metadata,
    Column("participante_id", Integer, ForeignKey("participante.id"), primary_key=True),
    Column("grupo_id", Integer, ForeignKey("grupo.id"), primary_key=True),
)
educador_grupo = Table(
    "educador_grupo",
    Base.metadata,
    Column("usuario_id", Integer, ForeignKey("usuario.id"), primary_key=True),
    Column("grupo_id", Integer, ForeignKey("grupo.id"), primary_key=True),
)

class Grupo(Base):
    __tablename__ = "grupos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(255))
    tipo_actividad = Column(String(100))
    rango_etario = Column(String(50))
    dias = Column(String(100))
    horario = Column(String(50))
    cupo_maximo = Column(Integer, default=30)

    creado_en = Column(DateTime, default=datetime.utcnow)
    actualizado_en = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    participantes = relationship(
        "Participante",
        secondary=participante_grupo,   
        backref="grupo"
     )
    educadores = relationship(
        "Usuario",
        secondary=educador_grupo,
        backref="grupos_asignados"
    )
    asistencias = relationship("Asistencia", backref="grupo")
    alertas = relationship("Alerta", backref="grupo")