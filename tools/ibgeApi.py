# Importa a biblioteca httpx para fazer requisições HTTP assíncronas
import httpx
# Importa o decorador 'tool' do LangChain para definir a função como uma ferramenta
from langchain_core.tools import tool

@tool
async def get_informacao_cidade(nome_cidade: str):
    """
    Busca dados estatísticos e códigos do IBGE para cidades brasileiras.
    Útil para informações oficiais e demográficas do Brasil.
    """
    # URL da API de municípios do IBGE
    url = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"
    
    # Usa um cliente HTTP assíncrono para fazer a requisição
    async with httpx.AsyncClient() as client:
        try:
            # Faz a requisição GET para a API
            response = await client.get(url, timeout=10)
            # Verifica se a requisição foi bem-sucedida
            if response.status_code == 200:
                cidades = response.json()
                # Procura a cidade na lista de cidades retornadas (ignorando maiúsculas/minúsculas)
                cidade_encontrada = next((c for c in cidades if c['nome'].lower() == nome_cidade.lower()), None)
                
                if cidade_encontrada:
                    # Retorna os dados da cidade encontrada como uma string
                    return str(cidade_encontrada)
                else:
                    return "Cidade não encontrada na base do IBGE."
            return "Erro na API do IBGE."
        except Exception as e:
            return f"Erro técnico IBGE: {str(e)}"