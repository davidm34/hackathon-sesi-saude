import shutil
import os
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# --- MODO PROTÓTIPO (Permitir Tudo) ---
# Isso diz ao navegador: "Pode deixar qualquer um acessar essa API"
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Aceita qualquer origem (3000, 5500, etc)
    allow_credentials=True,
    allow_methods=["*"],      # Aceita POST, GET, PUT, DELETE...
    allow_headers=["*"],      # Aceita qualquer cabeçalho
)
# ---------------------------------------

UPLOAD_DIR = "arquivos_recebidos"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)):
    # Caminho onde vai salvar
    file_location = os.path.join(UPLOAD_DIR, file.filename)

    # Salva o arquivo vindo do FormData direto no disco
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {"status": "ok", "mensagem": f"Arquivo salvo em {file_location}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)