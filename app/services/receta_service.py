# Lógica de negocio IA
import json
from app.ia.chains import chain_extraer, chain_receta
from app.schemas.receta_schema import PreferenciasUsuario,Preferencias  # Cambia aquí
from langchain_core.output_parsers import PydanticOutputParser

parser = PydanticOutputParser(pydantic_object=PreferenciasUsuario)
class RecetaService:
    async def generar_receta(self, mensaje: str) -> dict:
        # 1. Extraer con el parser automático
        try:
            raw_output = chain_extraer.invoke({"mensaje": mensaje})
            # Si chain_extraer ya incluye el parser, raw_output es una instancia de PreferenciasUsuario
            if isinstance(raw_output, PreferenciasUsuario):
                preferencias = raw_output
            else:
                # Fallback: intentar parsear como JSON
                try:
                    data = json.loads(raw_output)
                except:
                    # Limpiar markdown
                    if "```" in raw_output:
                        data = json.loads(raw_output.split("```")[1].split("```")[0])
                preferencias = PreferenciasUsuario(**data)
        except Exception as e:
            # Valores por defecto en caso de error
            preferencias = PreferenciasUsuario(
                ingredientes=["pollo"],
                restricciones=["desconocido"],
                tiempo=30
            )

        # 2. Convertir listas a strings para el prompt de receta
        ingredientes_str = ", ".join(preferencias.ingredientes) if preferencias.ingredientes else "pollo"
        restricciones_str = ", ".join(preferencias.restricciones) if preferencias.restricciones else "desconocido"

        # 3. Generar receta
        receta = chain_receta.invoke({
            "ingredientes": ingredientes_str,
            "restricciones": restricciones_str,
            "tiempo": preferencias.tiempo
        })

        # 4. Devolver respuesta (usando el schema original RecetaResponse requiere Preferencias, no PreferenciasUsuario)
        # Si RecetaResponse espera Preferencias, mapeamos:
        preferencias_simple = Preferencias(
            ingrediente=ingredientes_str,
            restricciones=restricciones_str,
            tiempo=preferencias.tiempo
        )

        return {
            "preferencias": preferencias_simple,
            "receta": receta
        }

receta_service = RecetaService()