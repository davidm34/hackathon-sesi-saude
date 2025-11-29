# hackathon-sesi-saude

## Instalação

1. Certifique-se de ter o **Python** instalado.
2. Abra o terminal na pasta do projeto.
3. Instale as dependências com o comando:

**Bash**

```
pip install -r requirements.txt
```

---

## Como Rodar

Você precisará de **dois terminais** abertos (um para o Backend e outro para o Frontend).

### Terminal 1: O Backend (API)

Este terminal rodará o FastAPI na porta  **8000** .

No terminal, execute:

**Bash**

```
python main.py
```

*Você verá uma mensagem como: `Uvicorn running on http://0.0.0.0:8000`*

### Terminal 2: O Frontend (Cliente)

Este terminal servirá o arquivo HTML na porta **3000** para simular um ambiente real.

No terminal, execute:

**Bash**

```
python -m http.server 3000
```

*Você verá uma mensagem como: `Serving HTTP on 0.0.0.0 port 3000`*

---

## Como Testar

1. Abra seu navegador e acesse: **http://localhost:3000**
2. Clique em "Escolher arquivo" e selecione um arquivo `.csv` do seu computador.
3. Clique no botão "Fazer Upload".
4. Verifique a pasta do projeto: uma nova pasta chamada `arquivos_recebidos` deve aparecer contendo o seu arquivo.
