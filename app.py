
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai

# Ottieni la chiave API dalle variabili di ambiente
openai.api_key = os.getenv("OPENAI_API_KEY")


# Crea l'app FastAPI
app = FastAPI()

# Configura il middleware CORS per permettere le richieste dal frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permette richieste da qualsiasi origine
    allow_credentials=True,
    allow_methods=["*"],  # Permette tutti i metodi HTTP
    allow_headers=["*"],  # Permette tutti gli header HTTP
)

# Modello per i dati ricevuti dal frontend
class RecommendationRequest(BaseModel):
    categoria: str
    descrizione: str

# Endpoint per generare raccomandazioni
@app.post("/raccomanda")
def raccomanda(request: RecommendationRequest):
    """
    Riceve la categoria e la descrizione, genera raccomandazioni utilizzando l'API OpenAI.
    """
    try:
        # Debug: stampa i dati ricevuti
        print("Dati ricevuti dal frontend:", request)

        # Prompt per il modello OpenAI
        prompt = f"""Sei un assistente esperto in raccomandazioni.
L'utente cerca {request.categoria}. Le sue preferenze sono: {request.descrizione}.
Genera un elenco di 5 raccomandazioni rilevanti con una breve spiegazione per ciascuna."""

        # Debug: stampa il prompt
        print("Prompt inviato a OpenAI:", prompt)

        # Richiesta al modello GPT
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Usa il modello desiderato
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
        raccomandazioni = response['choices'][0]['message']['content'].strip()
        return {"raccomandazioni": raccomandazioni}

    except openai.error.AuthenticationError as e:
        print("Errore di autenticazione con OpenAI:", e)
        raise HTTPException(status_code=401, detail="Chiave API OpenAI non valida o mancante.")

    except openai.error.OpenAIError as e:
        print("Errore generico OpenAI:", e)
        raise HTTPException(status_code=500, detail="Errore nella comunicazione con OpenAI.")

    except Exception as e:
        print("Errore sconosciuto:", e)
        raise HTTPException(status_code=500, detail=f"Errore interno del server: {e}")
