# Pydantic schemas
from pydantic import BaseModel, Field
from typing import List

class RecetaRequest(BaseModel):
    mensaje:str

class Preferencias(BaseModel):
    ingrediente:str
    restricciones:str
    tiempo:int

class RecetaResponse(BaseModel):
    preferencias: Preferencias
    receta:str

class PreferenciasUsuario(BaseModel):
    ingredientes: List[str] = Field(description="Lista de ingredientes principales mencionados por el usuario")
    restricciones: List[str] = Field(description="Lista de alergias, dietas o ingredientes prohibidos. Vacío si no hay.")
    tiempo: int = Field(description="Tiempo disponible en minutos. 0 si no se menciona.")
