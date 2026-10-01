from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.database import Base

class Material(Base):
    __tablename__ = "material"
    
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(255), nullable=False)
    descripcion = Column(String(500))
    categoria = Column(String(100))  
    ruta_archivo = Column(String(500), nullable=False)  
    usuario_id = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    grupo_id = Column(Integer, ForeignKey("grupo.id"))  
    
    creado_en = Column(DateTime, default=datetime.utcnow)
    actualizado_en = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)