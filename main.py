from fastapi import FastAPI, UploadFile, File
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
async def leer_pdf(file: UploadFile = File(...)):
    try:
        # Guarda el archivo temporalmente
        temp_path = f"./temp/{file.filename}"
        with open(temp_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Ejecuta el script con el archivo
        script_path = "./scripts/Leer_PDF.py"
        process = subprocess.Popen(
            ["python3", script_path, temp_path],
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