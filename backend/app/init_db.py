from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models.rol import Rol
from app.models.usuario import Usuario
from app.security.jwt_handler import JWTHandler

def init_db():
    """
    Inicializa la base de datos 
    """
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()

    try:
        if db.query(Rol).first():
            print("✅ Base de datos ya inicializada")
            return

        roles = [
            Rol(id=1, nombre="Coordinador", descripcion="Administrador del sistema"),
            Rol(id=2, nombre="Educador", descripcion="Responsable de grupos"),
            Rol(id=3, nombre="Participante", descripcion="Alumno participante"),
        ]
        
        db.add_all(roles)
        db.commit()

        coordinador = Usuario(
            email="admin@presente.plus",
            nombre="Admin",
            apellido="Sistema",
            password_hash=JWTHandler.hash_password("admin123"),
            rol_id=1,
            activo=True
        )
        
        db.add(coordinador)
        db.commit()
        
        print("✅ Base de datos inicializada correctamente")
        print("📧 Email: admin@presente.plus")
        print("🔑 Contraseña: admin123")
        
    except Exception as e:
        print(f"❌ Error al inicializar: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    init_db()