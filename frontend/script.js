document.getElementById("recommendationForm").addEventListener("submit", async function(event) {
    event.preventDefault(); // Impedisce il comportamento predefinito del form (ricaricamento della pagina)

    const categoria = document.getElementById("categoria").value;
    const descrizione = document.getElementById("descrizione").value;

    // Reset del campo risultato
    document.getElementById("risultato").textContent = "Caricamento...";

    try {
        const response = await fetch("https://fastapi-project-m05f.onrender.com/recommendations", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                tipo: categoria,
                genere: descrizione,
            }),
        });

        if (response.ok) {
            const data = await response.json();
            document.getElementById("risultato").textContent = data.recommendations || "Nessuna raccomandazione trovata.";
        } else {
            document.getElementById("risultato").textContent = "Errore durante la connessione al server.";
        }
    } catch (error) {
        console.error("Errore:", error);
        document.getElementById("risultato").textContent = "Errore durante la connessione al server.";
    }
});
