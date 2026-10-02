from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuario import Usuario
from app.security.jwt_handler import JWTHandler

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Usuario:
    """
    Dependencia para obtener el usuario actual a partir del token JWT.
    """
    token = credentials.credentials

    payload = JWTHandler.decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
        )

    email: str = payload.get("sub")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )
    
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado"
        )
    
    return usuario

def require_role(roles_permitidos: list[str]):
    """
    Crea una dependencia que valida que el usuario tenga uno de los roles permitidos.
    """
    async def check_role(
        usuario: Usuario = Depends(get_current_user),
        db: Session = Depends(get_db)
    ) -> Usuario:
        rol = db.query(str).from_statement(
            "SELECT nombre FROM rol WHERE id = :rol_id"
        ).params(rol_id=usuario.rol_id).first()
        
    
        if usuario.rol.nombre not in roles_permitidos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permiso insuficiente"
            )
        return usuario
    
    return check_role