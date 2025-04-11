from fastapi import FastAPI, Request
from pydantic import BaseModel
import subprocess
import os

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hola Railway desde FastAPI"}

class RutaPDFRequest(BaseModel):
    rutaPdf: str
    
@app.post("/leer-pdf")
async def leer_pdf(request: RutaPDFRequest):
    script_path = "./scripts/Leer_PDF.py"
    ruta_pdf = f"./temp/{request.rutaPdf}"

    try:
        process = subprocess.Popen(
            ["python3", script_path, ruta_pdf],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        stdout, stderr = process.communicate()

        if process.returncode != 0:
            return {"error": "Error en el script", "detalle": stderr}
        
        return {"resultado": stdout}

    except Exception as e:
        return {"error": "Error al ejecutar el script", "detalle": str(e)}
