import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Cache simples em memória para simular idempotência (Em produção, usa-se Redis ou Firestore)
PROCESSED_REQUESTS = set()

@app.route('/', methods=['GET', 'POST'])
def get_chuck_joke():
    # Obtém o cabeçalho de Idempotência
    idempotency_key = request.headers.get("X-Idempotency-Key")

    if idempotency_key and idempotency_key in PROCESSED_REQUESTS:
        return jsonify({
            "status": "SKIPPED",
            "message": "Requisição já processada anteriormente (Idempotente)."
        }), 200

    url = "https://api.chucknorris.io/jokes/random"
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        joke = data.get("value", "Nenhuma piada encontrada.")
        
        # Registra a chave como processada
        if idempotency_key:
            PROCESSED_REQUESTS.add(idempotency_key)

        return joke, 200, {'Content-Type': 'text/plain; charset=utf-8'}

    except requests.RequestException as e:
        return f"Erro ao buscar piada: {str(e)}", 500