from fastapi.testclient import TestClient
from app.main import app 

client = TestClient(app)

def test_health_check():
    """Testa se a rota raiz '/' está respondendo 200 OK."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "Service is running"}

def test_chat_endpoint_structure():
    """
    Testa se o endpoint de chat aceita o JSON correto.
    Nota: Não testamos a resposta do LLM aqui para não gastar créditos da API.
    Apenas verificamos se a API valida a entrada.
    """
    # Teste de erro proposital (payload vazio)
    response = client.post("/api/v1/chat", json={})
    assert response.status_code == 422 # Unprocessable Entity (Erro de validação)

def test_chat_flow_mock():
    """
    Exemplo avançado: Testa o fluxo completo.
    OBS: Isso vai realmente chamar o Gemini se não fizermos 'mock'.
    Para este teste, garantimos apenas que o status é 200 com uma pergunta simples.
    """
    payload = {"message": "Olá, quem é você?"}
    response = client.post("/api/v1/chat", json=payload)
    
    # Verifica se a requisição passou
    assert response.status_code == 200
    # Verifica se a resposta tem o campo esperado
    assert "response" in response.json()
    assert len(response.json()["response"]) > 0