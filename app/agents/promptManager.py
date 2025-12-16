import json
from datetime import datetime
from typing import List, Dict, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

# Define o nome do arquivo para armazenar o histórico de prompts
HISTORY_FILE = "prompt_history.json"
# Define o prompt padrão a ser usado se nenhum histórico for encontrado
DEFAULT_PROMPT = (
    "Você é GeoTravel, um agente de IA especializado em viagens, geografia e história mundial. "
    "Use as ferramentas disponíveis para obter dados em tempo real e o contexto para história. "
    "Mantenha a resposta concisa e informativa."
)

class PromptManager:
    """
    Gerencia o histórico de prompts do sistema, permitindo carregar, salvar,
    obter o prompt atual e atualizar com novos prompts.
    """
    def __init__(self):
        """Inicializa o gerenciador de prompts, carregando o histórico."""
        self._load_history()
    
    def _load_history(self):
        """Carrega o histórico de prompts do arquivo de persistência."""
        try:
            with open(HISTORY_FILE, 'r', encoding="utf-8") as f:
                self.history: List[Dict] = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Inicializa com o prompt padrão se o arquivo não existir ou estiver corrompido
            self.history = [{
                "id": 1,
                "timestamp": datetime.now().isoformat(),
                "prompt": DEFAULT_PROMPT,
                "reason": "Initial configuration"
            }]

    def _save_history(self):
        """Salva o histórico atual no arquivo."""
        with open (HISTORY_FILE, 'w', encoding="utf-8") as f:
            json.dump(self.history, f, indent= 4)

    def get_current_prompt(self) -> str:
        """Retorna o prompt do sistema mais recente."""
        # O último prompt da lista é o prompt atual
        return self.history[-1]["prompt"] if self.history else DEFAULT_PROMPT

    def get_history(self) -> List[Dict]:
        """Retorna todo o histórico de prompts."""
        return self.history
    
    def update_prompt(self, new_prompt: str, reason: str):
        """Adiciona um novo prompt ao histórico e o define como atual."""
        new_id = len(self.history) + 1
        new_entry = {
            "id": new_id,
            "timestamp": datetime.now().isoformat(),
            "prompt": new_prompt,
            "reason": reason
        }

        self.history.append(new_entry)
        self._save_history()
        return new_entry

# Cria uma instância única do PromptManager
prompt_manager = PromptManager() 

async def generate_new_prompt(old_prompt: str, user_feedback: str) -> str:
    """
    Usa um modelo de linguagem para analisar o feedback do usuário e gerar um 
    novo prompt de sistema otimizado.

    Args:
        old_prompt (str): O prompt de sistema anterior.
        user_feedback (str): O feedback fornecido pelo usuário.

    Returns:
        str: O novo prompt de sistema gerado, ou o prompt antigo em caso de erro.
    """
    # Configuração da LLM para a tarefa de Metaprompting
    llm_analyst = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)
    
    # Metaprompting (Instrução para a LLM)
    meta_system_prompt = (
        "Você é um Analista de IA focado em otimizar Prompts do Sistema para agentes de chat. "
        "Sua tarefa é analisar o 'Feedback do Usuário' e o 'Prompt Anterior' fornecidos. "
        "Com base no feedback, gere APENAS o novo e melhorado Prompt do Sistema, mantendo o tom e as instruções funcionais. "
        "Não inclua explicações ou floreios, apenas o texto limpo do novo prompt."
    )

    user_message = (
        f"PROMPT ANTERIOR: {old_prompt}\n\n"
        f"FEEDBACK DO USUÁRIO: {user_feedback}\n\n"
        "GERE O NOVO PROMPT DO SISTEMA MELHORADO:"
    )

    messages = [
        SystemMessage(content=meta_system_prompt),
        HumanMessage(content=user_message),
    ]

    # Execução da LLM
    try:
        response = await llm_analyst.ainvoke(messages)
        # O retorno é o novo prompt gerado pela LLM
        return response.content.strip()
    except Exception as e:
        print(f"Erro ao gerar novo prompt: {e}")
        return old_prompt # Retorna o prompt antigo em caso de falha