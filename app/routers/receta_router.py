# Endpoint / recetas
from fastapi import APIRouter
from app.schemas.receta_schema import RecetaRequest, RecetaResponse
from app.services.receta_service import receta_service


router= APIRouter(prefix="/recetas",tags=["recetas"])

@router.post("/generar",response_model=RecetaResponse)
async def generar_receta(request:RecetaRequest):
    resultado = await receta_service.generar_receta(request.mensaje)
    return resultado