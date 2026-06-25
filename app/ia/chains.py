# Chains de LangChain

from app.ia import llm
from app.ia.prompts import prompt_extraer, prompt_receta
from app.schemas.receta_schema import PreferenciasUsuario
from langchain_core.output_parsers import PydanticOutputParser,StrOutputParser

parser = PydanticOutputParser(pydantic_object=PreferenciasUsuario)

# Chain 1: Extraer preferncias
chain_extraer = prompt_extraer | llm | parser

# Chain 2: Generar receta
chain_receta = prompt_receta | llm | StrOutputParser()