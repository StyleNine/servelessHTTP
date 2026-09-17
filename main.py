import os
import json
import logging
import requests
from flask import Flask, request, jsonify

# Configuração de Logger para formato JSON
class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "severity": record.levelname,
            "message": record.getMessage(),
            "component": "chuck-norris-service",
            "environment": os.environ.get("ENV", "production")
        }
        # Injeta atributos extras passados no log
        if hasattr(record, "extra_fields"):
            log_record.update(record.extra_fields)
        return json.dumps(log_record)

handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())

logger = logging.getLogger("serverless-logger")
logger.setLevel(logging.INFO)
logger.addHandler(handler)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def process_event():
    # Captura da Chave de Idempotência enviada pelo Cloud Workflows
    idempotency_key = request.headers.get("X-Idempotency-Key", "N/A")
    
    extra = {
        "extra_fields": {
            "idempotency_key": idempotency_key,
            "http_method": request.method,
            "user_agent": request.headers.get("User-Agent")
        }
    }

    logger.info("Requisição recebida para processamento.", extra=extra)

    url = "https://api.chucknorris.io/jokes/random"

    try:
        response = requests.get(url, timeout=3)
        response.raise_for_status()
        data = response.json()
        joke = data.get("value", "")

        extra["extra_fields"]["status_code"] = 200
        extra["extra_fields"]["joke_id"] = data.get("id")
        logger.info("Piada obtida com sucesso da API externa.", extra=extra)

        return jsonify({
            "status": "success",
            "idempotency_key": idempotency_key,
            "joke": joke
        }), 200

    except requests.RequestException as e:
        extra["extra_fields"]["error_detail"] = str(e)
        logger.error("Falha ao se comunicar com a API externa.", extra=extra)
        return jsonify({
            "status": "error",
            "idempotency_key": idempotency_key,
            "message": "Erro na integração externa"
        }), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)