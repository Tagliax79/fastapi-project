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

@app.get("/recommendations/")
def get_recommendations(tipo: str, genere: str) -> Dict:
    """
    Chiamata a OpenAI API per ottenere raccomandazioni dinamiche.
    :param tipo: "film" o "serie_tv"
    :param genere: Genere del film o serie TV
    :return: Raccomandazioni generate dinamicamente
    """
    # Valida i parametri
    if tipo.lower() not in ["film", "serie_tv"]:
        return {"error": "Il tipo deve essere 'film' o 'serie_tv'."}

    # Prompt per OpenAI
    prompt = (
        f"Consiglia 5 {tipo} del genere {genere} che vale la pena vedere. "
        "Fornisci una lista di titoli con brevi descrizioni."
    )

    try:
        # Chiamata all'API di OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Sei un esperto di cinema e serie TV."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=150
        )
        # Estrai il testo della risposta
        recommendations = response["choices"][0]["message"]["content"]
        return {"recommendations": recommendations}
    except Exception as e:
        return {"error": f"Si è verificato un errore: {str(e)}"}
