# 1. Imagem Base: Usamos uma versão leve do Python 3.12 (Slim)
FROM python:3.12-slim

# 2. Diretório de Trabalho: Onde o código ficará dentro do contêiner
WORKDIR /app

# 3. Variáveis de Ambiente para otimizar o Python no Docker
# PYTHONDONTWRITEBYTECODE: Evita criar arquivos .pyc
# PYTHONUNBUFFERED: Garante que os logs apareçam instantaneamente no console
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 4. Instalação de Dependências
# Copiamos apenas o requirements.txt primeiro para aproveitar o cache do Docker
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 5. Cópia do Código Fonte
# Copia todo o resto do projeto para dentro da pasta /app
COPY . .

# 6. Exposição da Porta
# A aplicação roda na porta 8000, precisamos expô-la
EXPOSE 8000

# 7. Comando de Inicialização
# --host 0.0.0.0 é OBRIGATÓRIO no Docker (significa "aceitar conexões de fora do container")
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]