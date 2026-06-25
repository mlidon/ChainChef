from fastapi import FastAPI
from app.database import Base, engine
from app.models import user, book
from app.routers import auth_router, user_router, book_router,receta_router
from fastapi.middleware.cors import CORSMiddleware

#Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en desarrollo está bien
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(book_router.router)
app.include_router(receta_router.router)

@app.get("/")
def root():
    return {"message": "FastAPI funcionando correctamente en Windows"}