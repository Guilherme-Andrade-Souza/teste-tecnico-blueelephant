# 🌍 GeoTravel AI Agent

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?style=for-the-badge&logo=fastapi)
![LangChain](https://img.shields.io/badge/LangChain-v0.2-green?style=for-the-badge)
![Gemini](https://img.shields.io/badge/AI-Gemini%202.5-orange?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Concluído-success?style=for-the-badge)

## 📋 Visão Geral

O **GeoTravel AI Agent** é um assistente virtual inteligente projetado para atuar como um guia de viagens e especialista em geografia. Diferente de chatbots tradicionais, este agente possui **autonomia** para consultar ferramentas externas em tempo real e acessar uma base de conhecimento histórica (RAG).

O sistema é capaz de decidir *quando* precisa verificar a previsão do tempo, buscar dados demográficos no IBGE ou consultar informações gerais de países, entregando respostas precisas e contextualizadas.

## 🚀 Funcionalidades

- **🧠 Inteligência Artificial Generativa:** Utiliza o modelo **Google Gemini 1.5 Flash** para processamento de linguagem natural e raciocínio.
- **🛠️ Uso de Ferramentas (Tool Calling):**
  - **Clima em Tempo Real:** Integração com OpenWeatherMap API.
  - **Dados do Brasil:** Consulta automática à API de Localidades do IBGE.
  - **Dados Globais:** Informações de países via REST Countries API.
- **📚 Memória Contextual (RAG):** Utiliza **ChromaDB** para armazenar e recuperar informações históricas e culturais de um acervo local.
- **📝 Logs e Monitoramento:** Sistema de logging estruturado para rastreabilidade de erros e fluxo.
- **✅ Testes Automatizados:** Suíte de testes de integração com Pytest.

---

## ⚙️ Instalação e Configuração

### Pré-requisitos
- Python 3.10 ou superior.
- Conta no Google AI Studio (para obter a API Key).
- Conta no OpenWeatherMap (para obter a API Key).

### Passo a Passo

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/seu-usuario/teste-tecnico-blueelephant.git](https://github.com/seu-usuario/teste-tecnico-blueelephant.git)
   cd teste-tecnico-blueelephant