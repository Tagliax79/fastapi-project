document.getElementById('raccomandaForm').addEventListener('submit', async (e) => {
    e.preventDefault(); // Evita il refresh della pagina

    // Ottieni i valori dei campi
    const categoria = document.getElementById('categoria').value;
    const descrizione = document.getElementById('descrizione').value;

    // URL del backend FastAPI
   const url = 'https://tuo-progetto.onrender.com/raccomanda'; // Modifica dopo il deployment

    // Prepara i dati per la richiesta
    const dati = {
        categoria: categoria,
        descrizione: descrizione
    };

    try {
        // Invia la richiesta al backend
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(dati),
        });

        // Gestisci la risposta
        if (response.ok) {
            const json = await response.json();
            document.getElementById('risultati').innerText = json.raccomandazioni;
        } else {
            document.getElementById('risultati').innerText = `Errore: ${response.status}`;
        }
    } catch (error) {
        console.error('Errore:', error);
        document.getElementById('risultati').innerText = 'Errore durante la connessione al server.';
    }
});
