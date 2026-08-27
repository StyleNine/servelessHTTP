import base64
import requests
import json

def handle_pubsub_event(event, context):
    """
    Função disparada automaticamente quando uma mensagem é publicada no Pub/Sub.
    """
    # 1. Decodifica a mensagem recebida do Pub/Sub
    if 'data' in event:
        pubsub_message = base64.b64decode(event['data']).decode('utf-8')
        print(f"Mensagem recebida do Pub/Sub: {pubsub_message}")
    else:
        print("Mensagem Pub/Sub recebida sem corpo de dados.")

    # 2. Executa a lógica da API do Chuck Norris
    url = "https://api.chucknorris.io/jokes/random"
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        joke = data.get("value", "Nenhuma piada encontrada.")
        
        # Em arquiteturas orientadas a eventos, o resultado é enviado para os Logs (Cloud Logging)
        print(f"PIADA GERADA: {joke}")

    except requests.RequestException as e:
        print(f"Erro ao buscar piada da API: {str(e)}")