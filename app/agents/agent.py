# Importa as classes e funções necessárias do LangChain e outras bibliotecas
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor
from operator import itemgetter

# Importa as ferramentas personalizadas
from tools.restCountries import get_informacao_pais
from tools.openweathermap import get_clima_atual
from tools.ibgeApi import get_informacao_cidade
from vectorStore.db_manager import get_retriever
from app.utils.logger import setup_logger

# Template do prompt do sistema para o agente
SYSTEM_PROMPT_TEMPLATE = (
    "Você é GeoTravel, um agente de IA especializado em viagens, geografia e história mundial. "
    "Sua função é fornecer informações detalhadas, turísticas, históricas e climáticas. "
    "Use as ferramentas (Tools) disponíveis para obter dados em tempo real (Clima, Geografia, IBGE). "
    "Use o contexto da base de dados (Vector Store) para perguntas sobre história e cultura aprofundada. "
    "Mantenha a resposta concisa, informativa e profissional."
)

# Lista de ferramentas disponíveis para o agente
TOOLS_LIST = [
    get_informacao_pais,
    get_clima_atual,
    get_informacao_cidade
]

logger = setup_logger("GeoAgent")

class GeoTravelAgent:
    """
    A classe GeoTravelAgent encapsula a lógica para o agente de IA GeoTravel.
    """
    def __init__(self):
        """
        Inicializa o agente com o modelo de linguagem, prompt do sistema, ferramentas e retriever.
        """
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
        self.system_prompt = SYSTEM_PROMPT_TEMPLATE
        self.tools = TOOLS_LIST
        self.retriever = get_retriever()

    def get_executor(self, system_prompt: str):
        """
        Cria e retorna um executável de agente com o prompt do sistema fornecido.

        Args:
            system_prompt (str): O prompt do sistema para o agente.

        Returns:
            AgentExecutor: O executável do agente.
        """
        # Define o prompt do agente com placeholders para entrada do usuário e rascunho do agente
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

        # Cria o agente usando o modelo de linguagem, ferramentas e prompt
        agent = create_tool_calling_agent(self.llm, self.tools, prompt)

        # Cria o executável do agente
        return AgentExecutor(agent=agent, tools=self.tools, verbose=True)

    async def run_agent(self, user_question: str, current_system_prompt: str):
        """
        Executa a orquestração do Agente.

        Args:
            user_question (str): A pergunta do usuário.
            current_system_prompt (str): O prompt do sistema atual.

        Returns:
            str: A resposta do agente.
        """
        executor = self.get_executor(current_system_prompt)
        
        logger.info(f"Recebendo pergunta: '{user_question}")

        try:
            # O input deve ser passado como dicionário com a chave "input"
            payload = {"input": user_question}
            
            # Executa o agente
            response = await executor.ainvoke(payload)
            
            logger.info("Resposta gerada com sucesso.")

            return response["output"]
            
        except Exception as e:
            #Logando erro com traceback
            logger.error(f"Falha na execução do agente: {e}", exc_info=True)
            return f"Erro ao processar sua solicitação: {e}"