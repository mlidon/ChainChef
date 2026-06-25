import sys
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.database import Base, engine
from app.models import user
from app.routers import auth_router, user_router,receta_router
from fastapi.middleware.cors import CORSMiddleware


# ---------- FRONTEND PATH ----------
def get_frontend_path():
    """Devuelve la ruta absoluta a la carpeta frontend, funcione donde funcione"""
    if getattr(sys, 'frozen', False):
        # Ejecutando como .exe empaquetado
        base_path = sys._MEIPASS
    else:
        # Ejecutando como script normal
        base_path = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(base_path, 'frontend')



# ---------- DB ----------
Base.metadata.create_all(bind=engine)
# ---------- APP ----------
app = FastAPI()


# ---------- CORS ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en desarrollo está bien
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- ROUTERS ----------
app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(receta_router.router)

# ---------- STATIC FILES (SIEMPRE AL FINAL) ----------
frontend_path = get_frontend_path()
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
else:
    @app.get("/")
    def root():
        return {"message": "FastAPI funcionando pero no se encontró frontend en " + frontend_path}

