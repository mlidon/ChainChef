# Configuración del modelo 
from langchain_ollama import ChatOllama


# Modelo compartido para todas las chains
llm = ChatOllama(
    model = "llama3:instruct",
    temperature=0.7,
    base_url="http://localhost:11434"
)