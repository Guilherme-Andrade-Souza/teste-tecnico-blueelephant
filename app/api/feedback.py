# Importa as classes e funções necessárias do FastAPI, Pydantic e do gerenciador de prompts
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.agents.promptManager import prompt_manager, generate_new_prompt

# Cria um roteador FastAPI para os endpoints de feedback
router = APIRouter()

class FeedbackRequest(BaseModel):
    """Modelo Pydantic para a requisição de feedback."""
    feedback_text: str
    
class FeedbackResponse(BaseModel):
    """Modelo Pydantic para a resposta de feedback."""
    status: str
    new_prompt: str
    
@router.post("/feedback", response_model=FeedbackResponse)
async def process_feedback(request: FeedbackRequest):
    """
    Endpoint para receber feedback, processá-lo e atualizar o prompt do agente.
    """
    if not request.feedback_text.strip():
        raise HTTPException(status_code=400, detail="O feedback não pode estar vazio.")

    # 1. Obter o prompt atual antes da modificação
    old_prompt = prompt_manager.get_current_prompt()
    
    # 2. Lógica Inteligente: Usar a LLM para gerar o novo prompt
    new_prompt_content = await generate_new_prompt(old_prompt, request.feedback_text)
    
    # 3. Atualizar o Prompt Manager
    # A razão do update é o próprio feedback do usuário
    updated_entry = prompt_manager.update_prompt(
        new_prompt=new_prompt_content, 
        reason=f"Feedback do usuário: {request.feedback_text[:100]}..."
    )
    
    return FeedbackResponse(
        status="success", 
        new_prompt=updated_entry["prompt"]
    )