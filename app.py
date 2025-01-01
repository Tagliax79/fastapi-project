
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
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

# Monta StaticFiles su /static
app.mount("/static", StaticFiles(directory="frontend", html=True), name="static")

# Modello per i dati ricevuti dal frontend
class RecommendationRequest(BaseModel):
    tipo: str  # Es. "risultati" o "calciomercato"
    genere: str  # Es. "Campionato", "Championms League", ecc.

# Endpoint per il messaggio di benvenuto
@app.get("/api")
def read_root():
    return {"message": "Benvenuto nell'API per le raccomandazioni dinamiche!"}

# Endpoint per generare raccomandazioni
@app.post("/api/recommendations")
def generate_recommendations(request: RecommendationRequest):
    """
    Riceve il tipo e il genere, genera raccomandazioni utilizzando l'API OpenAI.
    """
    try:
        # Debug: stampa i dati ricevuti
        print("Dati ricevuti:", request)

        # Crea il prompt per il modello OpenAI
        prompt = f"""Sei un assistente esperto in ricerca notizie sull'AC Milan.
L'utente sta cercando {request.tipo} di genere {request.genere}.
Genera un elenco di 6 notizie rilevanti, cercando solo sul sito di www.milannews.it e www.acmilan.com. Quando rispondi inserisci il link della singola notizia trovata. Cerca sempre notizie relative alla giornata odierna"""

        # Debug: stampa il prompt
        print("Prompt inviato a OpenAI:", prompt)

        # Richiesta al modello OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Sei un assistente esperto in ricerca notizie sull'AC Milan."},
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

# Endpoint per servire index.html sulla root "/"
@app.get("/", response_class=HTMLResponse)
async def serve_index():
    try:
        with open("frontend/index.html", "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print("Errore nel servire index.html:", e)
        raise HTTPException(status_code=500, detail="Errore nel servire la pagina principale.")
