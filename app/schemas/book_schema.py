from pydantic import BaseModel
from typing import Optional

# -----------------------------
# Esquemas de entrada
# -----------------------------

class BookCreate(BaseModel):
    title:str
    author:str
    year:int
    image_url:Optional[str]=None


class BookUpdate(BaseModel):
    title: str
    author: str
    year: int
    image_url: Optional[str] = None



# -----------------------------
# Esquemas de salida
# -----------------------------

class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    year: int
    image_url: Optional[str]
    owner_id: int

    class Config:
        from_attributes = True