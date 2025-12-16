# 🌍 GeoTravel AI Agent

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
![Gemini](https://img.shields.io/badge/AI-Gemini%202.5-orange?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?style=for-the-badge&logo=fastapi)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=for-the-badge&logo=docker)
![LangChain](https://img.shields.io/badge/LangChain-v0.2-green?style=for-the-badge)

## 📖 Sobre o Projeto

O **GeoTravel AI Agent** é um assistente virtual autônomo especializado em turismo, geografia e história. 

Utilizando o **Google Gemini 2.5 Flash** orquestrado pelo **LangChain**, o agente não apenas conversa, mas **age**: ele decide autonomamente quando consultar APIs de clima em tempo real, buscar dados demográficos no IBGE ou acessar uma base de conhecimento histórica local (RAG).

### 🚀 Funcionalidades Principais
- **Orquestração de Ferramentas:** Decide sozinho se usa ferramentas externas ou conhecimento interno.
- **Clima em Tempo Real:** Integração com OpenWeatherMap.
- **Dados Oficiais:** Integração com APIs do IBGE e REST Countries.
- **Memória Contextual (RAG):** Recuperação de informações históricas via ChromaDB.
- **API Documentada:** Swagger UI nativo.

---

## 🛠️ Tecnologias Utilizadas

- **Core:** Python 3.12
- **Framework Web:** FastAPI + Uvicorn
- **IA Generativa:** Google Gemini 2.5 Flash
- **Orquestração:** LangChain (Agents & Tools)
- **Banco Vetorial:** ChromaDB
- **Infraestrutura:** Docker & Docker Compose
- **Testes:** Pytest

---

## Quick Start (Resumo)

**Pré-requisitos:** Docker e Docker Compose.

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/SEU-USUARIO/geotravel-agent.git](https://github.com/SEU-USUARIO/geotravel-agent.git)
   cd geotravel-agent

2.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure as variáveis de ambiente:**

    Copie o arquivo `.env_exemplo` para `.env` e adicione suas chaves de API:
    ```bash
    cp .env_exemplo .env
    ```
    Edite o arquivo `.env` com suas chaves:
    ```
    GOOGLE_API_KEY="SUA_CHAVE_API_DO_GOOGLE"
    OPENWEATHER_API_KEY="SUA_CHAVE_API_DO_OPENWEATHERMAP"
    ```

### Execução

1.  **Inicie o servidor da API:**
    ```bash
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    ```

2.  **Acesse a interface do usuário:**

    Abra o arquivo `frontend/index.html` em seu navegador.

## Instruções para rodar com Docker

### Pré-requisitos

- Docker
- Docker Compose

### Execução

1.  **Construa e inicie os contêineres:**

    A partir da raiz do projeto, execute:
    ```bash
    docker-compose up --build
    ```

    O serviço estará disponível em `http://localhost:8000`. A interface do usuário pode ser acessada abrindo `frontend/index.html` no navegador, que se comunicará com a API em `localhost:8000`.

## Exemplos de uso

Após iniciar a aplicação, abra o arquivo `frontend/index.html` no seu navegador.

-   **Chat com o Agente:**
    -   Na aba "Agent Chat", digite sua pergunta sobre viagens.
    -   Exemplos:
        -   "Qual o clima atual em São Paulo?"
        -   "Me dê informações sobre o Brasil."
        -   "Qual o código do IBGE para a cidade de Salvador?"

-   **Fornecer Feedback:**
    -   Vá para a aba "Feedback and Improvement".
    -   Você verá o prompt de sistema atual do agente.
    -   No campo de feedback, descreva como a última resposta poderia ser melhor.
    -   Clique em "Send Feedback". O sistema irá gerar e aplicar um novo prompt para o agente.

## Documentação das APIs utilizadas

### APIs Internas (GeoTravel API)

A API é construída com FastAPI e está disponível em `http://localhost:8000`.

-   **`POST /api/v1/chat`**:
    -   **Descrição:** Envia uma mensagem para o agente de IA e recebe uma resposta.
    -   **Request Body:**
        ```json
        {
          "message": "string"
        }
        ```
    -   **Response Body:**
        ```json
        {
          "response": "string"
        }
        ```

-   **`POST /api/v1/feedback`**:
    -   **Descrição:** Envia um feedback sobre a resposta do agente para melhorar o prompt do sistema.
    -   **Request Body:**
        ```json
        {
          "feedback_text": "string"
        }
        ```
    -   **Response Body:**
        ```json
        {
          "status": "string",
          "new_prompt": "string"
        }
        ```

-   **`GET /`**:
    -   **Descrição:** Endpoint de health check para verificar se o serviço está rodando.
    -   **Response Body:**
        ```json
        {
          "status": "ok",
          "message": "Serviço esta rodando"
        }
        ```

### APIs Externas

O agente utiliza as seguintes APIs para buscar informações:

-   **OpenWeatherMap API**:
    -   **Função:** `get_clima_atual(city_name: str)`
    -   **Descrição:** Busca as condições climáticas atuais para uma cidade específica.
    -   **Endpoint:** `http://api.openweathermap.org/data/2.5/weather`

-   **REST Countries API**:
    -   **Função:** `get_informacao_pais(country_name: str)`
    -   **Descrição:** Fornece informações gerais sobre um país, como capital, população e moeda.
    -   **Endpoint:** `https://restcountries.com/v3.1/name/{country_name}`

-   **IBGE API**:
    -   **Função:** `get_informacao_cidade(nome_cidade: str)`
    -   **Descrição:** Busca dados estatísticos e códigos do IBGE para cidades brasileiras.
    -   **Endpoint:** `https://servicodados.ibge.gov.br/api/v1/localidades/municipios`