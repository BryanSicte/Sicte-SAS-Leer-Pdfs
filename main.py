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
    temp_folder = "./temp"
    os.makedirs(temp_folder, exist_ok=True)

    ruta_pdf = os.path.join(temp_folder, file.filename)

    with open(ruta_pdf, "wb") as f:
        content = await file.read()
        f.write(content)

    try:
        process = subprocess.Popen(
            ["python3", "./scripts/Leer_PDF.py", ruta_pdf],
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