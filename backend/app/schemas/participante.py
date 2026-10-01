from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class TutorCreate(BaseModel):
    nombre: str
    apellido: str
    email: str
    telefono: Optional[str]= [None]
    relacion: Optional[str] = [None]

class ParticipanteBase(BaseModel):
    dni: str
    fecha_nacimiento: Optional[str] = [None]
    domicilio: Optional[str] = [None]
    telefono: Optional[str] = [None]
    estado = str = "activo"

class ParticipanteCreate(ParticipanteBase):
    usuario_id: int
    tutor: Optional[list[TutorCreate]] = None

class ParticipanteResponse(ParticipanteBase):
    id: int
    usuario_id: int
    creado_en: datetime

    class Config:
        from_attributes = True

class ParticipanteLegajo(ParticipanteResponse):
    """Vista completa del legajo digital"""
    nombre: str
    apellido: str
    tutores: list
    grupos: list