import os
import shutil
from datetime import datetime
from typing import List, Any
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import openpyxl
import xlrd # Necessário para ler arquivos .xls antigos

app = FastAPI()

# --- Configuração CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Diretórios
UPLOAD_DIR = "arquivos_recebidos"
OUTPUT_DIR = "arquivos_gerados"

# Nomes esperados para o modelo
TEMPLATE_XLSX = "modelo.xlsx"
TEMPLATE_XLS = "modelo.xls"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

class DadosPlanilha(BaseModel):
    dados: List[List[Any]]

def carregar_modelo():
    """
    Tenta carregar o modelo. 
    Se for .xlsx, usa openpyxl direto.
    Se for .xls, usa xlrd para ler e converte para openpyxl.
    """
    # 1. Tenta carregar .xlsx (Preferencial)
    if os.path.exists(TEMPLATE_XLSX):
        print(f"Usando modelo .xlsx: {TEMPLATE_XLSX}")
        return openpyxl.load_workbook(TEMPLATE_XLSX)
    
    # 2. Se não houver, tenta carregar .xls e converter
    elif os.path.exists(TEMPLATE_XLS):
        print(f"Modelo .xls encontrado: {TEMPLATE_XLS}. Convertendo dados...")
        try:
            # Lê o arquivo antigo
            rb = xlrd.open_workbook(TEMPLATE_XLS)
            sheet_old = rb.sheet_by_index(0)
            
            # Cria um novo workbook moderno em memória
            wb_new = openpyxl.Workbook()
            ws_new = wb_new.active
            ws_new.title = "Modelo 1" # Ou sheet_old.name

            # Copia os dados do antigo para o novo (célula a célula)
            for r in range(sheet_old.nrows):
                row_values = sheet_old.row_values(r)
                ws_new.append(row_values)
            
            return wb_new
        except Exception as e:
            raise Exception(f"Erro ao converter .xls: {str(e)}")
    
    else:
        return None

@app.post("/gerar-excel/")
def gerar_excel(payload: DadosPlanilha):
    try:
        wb = carregar_modelo()
        
        if wb is None:
             return {
                 "status": "erro", 
                 "mensagem": f"Nenhum arquivo modelo encontrado. Adicione '{TEMPLATE_XLSX}' ou '{TEMPLATE_XLS}' na pasta."
             }

        ws = wb.active

        # Descobre a próxima linha vazia
        # Nota: Se convertemos de .xls, o append já preencheu as linhas.
        start_row = ws.max_row + 1

        # Adiciona os novos dados recebidos do frontend
        for row_data in payload.dados:
            ws.append(row_data)

        # Gera nome do arquivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Exportacao_eSocial_{timestamp}.xlsx"
        file_path = os.path.join(OUTPUT_DIR, filename)

        # Salva como .xlsx (Sempre salvamos no formato novo)
        wb.save(file_path)
        print(f"Arquivo gerado: {file_path}")

        return {
            "status": "ok", 
            "mensagem": f"Arquivo gerado com sucesso em: {file_path}",
            "arquivo": filename
        }

    except Exception as e:
        print(f"Erro crítico: {e}")
        return {"status": "erro", "mensagem": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)