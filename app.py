
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import openai
import os

# Configura la chiave API di OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Crea l'app FastAPI
app = FastAPI()

# Middleware CORS per permettere le richieste dal frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permette richieste da qualsiasi origine
    allow_credentials=True,
    allow_methods=["*"],  # Permette tutti i metodi HTTP
    allow_headers=["*"],  # Permette tutti gli header HTTP
)

# Configura la cartella dei file statici (frontend)
app.mount("/", StaticFiles(directory="frontend", html=True), name="static")

# Modello per i dati ricevuti dal frontend
class RecommendationRequest(BaseModel):
    tipo: str  # Es. "film" o "serie tv"
    genere: str  # Es. "azione", "commedia", ecc.

# Endpoint per il messaggio di benvenuto
@app.get("/")
def read_root():
    return {"message": "Benvenuto nell'API per le raccomandazioni dinamiche!"}

# Endpoint per generare raccomandazioni
@app.post("/recommendations")
def generate_recommendations(request: RecommendationRequest):
    """
    Riceve il tipo e il genere, genera raccomandazioni utilizzando l'API OpenAI.
    """
    try:
        # Debug: stampa i dati ricevuti
        print("Dati ricevuti:", request)

        # Crea il prompt per il modello OpenAI
        prompt = f"""Sei un assistente esperto in raccomandazioni personalizzate.
L'utente sta cercando {request.tipo} di genere {request.genere}.
Genera un elenco di 5 raccomandazioni rilevanti, con una breve spiegazione per ciascuna."""

        # Debug: stampa il prompt
        print("Prompt inviato a OpenAI:", prompt)

        # Richiesta al modello OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Sei un assistente esperto in raccomandazioni personalizzate."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7,
        )

        # Debug: stampa la risposta grezza
        print("Risposta grezza da OpenAI:", response)

        # Estrai la risposta generata
        recommendations = response['choices'][0]['message']['content'].strip()
        return {"recommendations": recommendations}

    except openai.error.AuthenticationError as e:
        print("Errore di autenticazione con OpenAI:", e)
        raise HTTPException(status_code=401, detail="Chiave API OpenAI non valida o mancante.")

    except openai.error.OpenAIError as e:
        print("Errore generico OpenAI:", e)
        raise HTTPException(status_code=500, detail="Errore nella comunicazione con OpenAI.")

    except Exception as e:
        print("Errore sconosciuto:", e)
        raise HTTPException(status_code=500, detail=f"Errore interno del server: {e}")
