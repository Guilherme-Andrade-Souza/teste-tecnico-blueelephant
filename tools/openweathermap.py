# Importa as bibliotecas os e httpx para manipulação de variáveis de ambiente e requisições HTTP
import os
import httpx
# Importa o decorador 'tool' do LangChain para definir a função como uma ferramenta
from langchain_core.tools import tool

@tool
async def get_clima_atual(city_name: str):
    """
    Busca as condições climáticas atuais para uma cidade específica.
    Retorna temperatura, descrição do clima e umidade.
    """
    # Obtém a chave da API do OpenWeatherMap das variáveis de ambiente
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return "Erro: API Key não configurada."

    # Monta a URL da API com o nome da cidade e a chave da API
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric&lang=pt_br"
    
    # Usa um cliente HTTP assíncrono para fazer a requisição
    async with httpx.AsyncClient() as client:
        try:
            # Faz a requisição GET para a API
            response = await client.get(url, timeout=10)
            # Verifica se a requisição foi bem-sucedida
            if response.status_code == 200:
                data = response.json()
                # Retorna uma string formatada com as informações do clima
                return (f"Clima em {city_name}: {data['weather'][0]['description']}, "
                        f"Temperatura: {data['main']['temp']}°C, "
                        f"Umidade: {data['main']['humidity']}%")
            else:
                return f"Não foi possível obter o clima. Status: {response.status_code}"
        except Exception as e:
            return f"Erro na conexão com API de clima: {str(e)}"