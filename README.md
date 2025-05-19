Progetto di Programmazione di Reti - **Traccia 1: Web Server + Sito Statico**
Titolo: **Mini-Webserver - Autoscuola Marte**
Studente: Matteo Onofri 
matricola: 0001091274


## Requisiti
Python **3.12** o superiore

## Avvio del server

python3 server.py

## Utilizzo

- Il server serve i file statici presenti nella cartella `www`.
- La Homepage è `index.html`.
- Se un file non viene trovato, viene restituita la pagina `404.html` che reindirizza alla homepage.
- I log degli accessi vengono salvati in `access.log`.

## Note

- È protetto da directory traversal (`..` nel percorso).
- Rileva automaticamente il tipo MIME dei file serviti.