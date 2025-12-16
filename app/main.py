# Importa as bibliotecas necessárias
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.api import chat as chat_router
from app.api import feedback as feedback_router

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Cria a instância principal da aplicação FastAPI
app = FastAPI (
    title = "GeoTravel",
    descriptuin= "Sistema de Agente de IA para viagens com feedback dinâmico."
)

# Configura o CORS para permitir requisições de qualquer origem
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui as rotas da API de chat
app.include_router(chat_router.router, prefix="/api/v1")
# Inclui as rotas da API de feedback
app.include_router(feedback_router.router, prefix="/api/v1")

# Define a rota principal para teste de saúde da conexão
@app.get("/")
def teste_saude_conexao():
    """
    Endpoint de health check para verificar se o serviço está rodando.
    """
    return {"status": "ok", "message": "Serviço esta rodando"}