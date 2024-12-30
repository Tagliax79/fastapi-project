import os
from fastapi import FastAPI
import openai
from typing import List, Dict

app = FastAPI()

# Ottieni la chiave API dalle variabili di ambiente
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Dynamic Film and Series Recommendation API!"}

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Monta la cartella frontend come statica
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

@app.get("/api/recommendations")
async def get_recommendations(tipo: str, genere: str):
    # Qui va la logica delle tue raccomandazioni
    return {"message": "Funziona tutto correttamente!"}
