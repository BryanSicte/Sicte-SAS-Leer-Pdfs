from fastapi import FastAPI, UploadFile, File
import subprocess
import os
import json  # Importar el módulo json para trabajar con JSON

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hola Railway desde FastAPI"}

@app.post("/leer-pdf")
async def leer_pdf(file: UploadFile = File(...)):
    try:
        # Crea el directorio 'temp' si no existe
        os.makedirs("./temp", exist_ok=True)

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

        # Convertir el resultado a un objeto JSON
        try:
            resultado_json = json.loads(stdout)  # Convertimos la cadena a JSON
            return {"resultado": resultado_json}  # Devolvemos el JSON
        except json.JSONDecodeError as e:
            return {"error": "Error al convertir el resultado a JSON", "detalle": str(e)}

    except Exception as e:
        return {"error": "Error al ejecutar el script", "detalle": str(e)}