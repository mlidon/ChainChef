# run_server.py
import os
import sys
import uvicorn
import webbrowser
import threading
import time

def open_browser():
    """Abre el navegador después de un breve retardo"""
    time.sleep(2)
    webbrowser.open("http://127.0.0.1:8000/recetas.html")

if __name__ == "__main__":
    # Iniciar el servidor en un hilo separado
    threading.Thread(target=open_browser, daemon=True).start()
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, log_level="info")