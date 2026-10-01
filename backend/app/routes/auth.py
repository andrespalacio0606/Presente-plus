from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuario import Usuario
from app.models.rol import Rol
from app.schemas.usuario import UsuarioLogin, UsuarioCreate, TokenResponse, UsuarioResponse
from app.security.jwt_handler import JWTHandler

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/login", response_model=TokenResponse)
def login(
    credentials: UsuarioLogin,
    db: Session = Depends(get_db),
):
    """
    Endpoint de login.
    Retorna un token JWT si lasa credenciales son correctas.
    """
    usuario = db.query(Usuario).filter(
        Usuario.email == credentials.email
        ).first()

    if not usuario or not usuario.activo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
        )
    if not JWTHandler.verify_password(
        credentials.password,
        usuario.password
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales inválidas",
        )

    token = JWTHandler.create_access_token(
        data={"sub": usuario.email, "rol_id": usuario.rol_id}
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "usuario": UsuarioResponse.from_orm(usuario),
    }

@router.post("/register", response_model=UsuarioResponse)
def register(
    datos: UsuarioCreate,
    db: Session = Depends(get_db)
):
    """
    Endpoint de registro de nuevos usuarios.
    Crea un usuario con contraseña hasheada.
    """
    usuario_existente = db.query(Usuario).filter(
        Usuario.email == datos.email
    ).first()

    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado",
        )

    rol = db.query(Rol).filter(Rol.id == datos.rol_id).first()
    if not rol:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rol no válido",
        )

    nuevo_usuario = Usuario(
        email=datos.email,
        nombre=datos.nombre,
        apellido=datos.apellido,
        password_hash=JWTHandler.hash_password(datos.password),
        rol_id=datos.rol_id,
        activo=True
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    token = JWTHandler.create_access_token(
        data={"sub": nuevo_usuario.email, "rol_id": nuevo_usuario.rol_id}
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "usuario": UsuarioResponse.from_orm(nuevo_usuario),
    }