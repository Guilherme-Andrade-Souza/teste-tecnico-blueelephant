from fastapi import APIRouter
from pydantic import BaseModel
from app.agents.agent import GeoTravelAgent

# Cria um roteador FastAPI para os endpoints de chat
router = APIRouter()
# Cria uma instância do agente GeoTravel
agent = GeoTravelAgent()

class ChatRequest(BaseModel):
    """
    Modelo Pydantic para a requisição de chat, esperando uma única mensagem de texto.
    """
    message: str

class ChatResponse(BaseModel):
    """
    Modelo Pydantic para a resposta do chat, retornando a resposta do agente.
    """
    response: str

@router.post("/chat", response_model=ChatResponse)
async def process_chat(request: ChatRequest):
    """
    Endpoint principal para interagir com o agente de IA GeoTravel.
    Recebe uma mensagem do usuário, processa através do agente e retorna a resposta.
    """
    # Obtém o prompt de sistema atual do agente
    current_prompt = agent.system_prompt

    try:
        # Executa o agente com a mensagem do usuário e o prompt atual
        response_text = await agent.run_agent(request.message, current_prompt)
        return ChatResponse(response=response_text)
    except Exception as e:
        # Retorna uma mensagem de erro se o processamento do agente falhar
        return ChatResponse(response=f"Erro no processamento do Agente: {str(e)}")