from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.config import settings
from app.routes import api_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Presente Plus API",
    description="API para la gestión de participantes, asistencia ",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    # # URLs del frontend
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

@app.get("/")
def read_root():
    return {"message": "Bienvenido a Presente+ API", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "environment": settings.environment}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)