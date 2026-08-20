import os
import httpx
from fastapi import FastAPI, HTTPException

app = FastAPI()

# URL oficial da API do Chuck Norris
CHUCK_API_URL = "https://api.chucknorris.io/jokes/random"

@app.get("/")
async def get_chuck_joke():
    # Usamos httpx.AsyncClient para fazer requisições de forma não-bloqueante
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(CHUCK_API_URL)
            response.raise_for_status()  # Lança exceção se a API responder com erro
            
            # Decodifica o JSON retornado pela API do Chuck Norris
            data = response.json()
            
            # Retorna apenas a piada (o campo "value" do JSON)
            return {"joke": data.get("value")}
        
        except httpx.HTTPError as e:
            # Tratamento caso a API externa falhe
            raise HTTPException(status_code=502, detail=f"Erro ao consultar a API do Chuck Norris: {str(e)}")

if __name__ == "__main__":
    # O Cloud Run injeta a porta através da variável de ambiente PORT (padrão 8080)
    port = int(os.environ.get("PORT", 8080))
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)