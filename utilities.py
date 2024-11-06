import os
import sys
from dotenv import load_dotenv

# Carica le variabili d'ambiente dal file .env
load_dotenv()

# Funzione per verificare la presenza delle variabili necessarie per configurare OpenAI e l'assistant
def check_openai_env_variables():
    required_vars = ["AZURE_OPENAI_ENDPOINT", "AZURE_OPENAI_API_KEY", "ASSISTANT_ID"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        alert_message = f"ALERT: Variabili mancanti o non caricate correttamente nel .env: {', '.join(missing_vars)}"
        print(alert_message)
        send_alert(alert_message)
        sys.exit("Errore: variabili d'ambiente mancanti. Terminazione del programma.")
    else:
        print("Tutte le variabili d'ambiente per OpenAI sono presenti e caricate correttamente.")

# Funzione per inviare un alert (può essere un log o una notifica)
def send_alert(message):
    print(f"ALERT: {message}")  # Messaggio di alert in console
    # Qui puoi aggiungere codice per inviare email o registrare log se necessario
