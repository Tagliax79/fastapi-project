from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import openai
import os

# Configura la chiave API di OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Crea l'app FastAPI
app = FastAPI()

# Configura CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permette richieste da tutti i domini (per sviluppo). Puoi specificare ["https://tuo-dominio.com"]
    allow_credentials=True,
    allow_methods=["*"],  # Permette tutti i metodi HTTP (GET, POST, ecc.)
    allow_headers=["*"],  # Permette tutti gli header
)

import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import openai

# Ottieni la chiave API dalle variabili di ambiente
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# Monta la cartella frontend come statica
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Dynamic Film and Series Recommendation API!"}

@app.post("/recommendations")
async def get_recommendations(tipo: str, genere: str):
    # Esempio di chiamata API con OpenAI
    prompt = f"Dammi i migliori 5 {tipo} del genere {genere}."
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
        )
        recommendations = response.choices[0].text.strip()
        return {"recommendations": recommendations}
    except Exception as e:
        return {"error": str(e)}
