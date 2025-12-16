# Importa a biblioteca httpx para fazer requisições HTTP assíncronas
import httpx
# Importa o decorador 'tool' do LangChain para definir a função como uma ferramenta
from langchain_core.tools import tool

@tool
async def get_informacao_pais(country_name: str):
    """
    Fornece informações gerais sobre um país, como capital, população e moeda.
    Use o nome do país em inglês ou português.
    """
    # Monta a URL da API RestCountries com o nome do país
    url = f"https://restcountries.com/v3.1/name/{country_name}"
    
    # Usa um cliente HTTP assíncrono para fazer a requisição
    async with httpx.AsyncClient() as client:
        try:
            # Faz a requisição GET para a API
            response = await client.get(url, timeout=10)
            # Verifica se a requisição foi bem-sucedida
            if response.status_code == 200:
                data = response.json()[0]
                # Extrai informações relevantes para evitar exceder o limite de contexto
                info = {
                    "nome": data.get("name", {}).get("common"),
                    "capital": data.get("capital", ["N/A"])[0],
                    "populacao": data.get("population"),
                    "regiao": data.get("region")
                }
                # Retorna as informações como uma string
                return str(info)
            else:
                return f"País não encontrado. Verifique a grafia."
        except Exception as e:
            return f"Erro ao buscar país: {str(e)}"