# Imagem base leve e oficial do Python
FROM python:3.11-slim

# Evita que o Python grave arquivos .pyc no disco
ENV PYTHONDONTWRITEBYTECODE=1
# Garante que os logs sejam exibidos imediatamente no Cloud Run
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instala as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY app.py .

# Comando de inicialização
CMD ["python", "app.py"]