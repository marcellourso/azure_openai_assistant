import openai
from openai import AzureOpenAI
import requests
import time
import os
from utilities import check_openai_env_variables

# Esegui il controllo delle variabili specifiche per OpenAI
check_openai_env_variables()

# Configura OpenAI con l'assistant ID esistente solo se tutte le variabili sono presenti
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")
assistant_id = os.getenv("ASSISTANT_ID")

# Inizializza il client Azure OpenAI con le configurazioni esistenti
client = AzureOpenAI(
  azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
  api_key=os.getenv("AZURE_OPENAI_API_KEY"),
  api_version="2024-05-01-preview"
)

# Assistant ID già creato tramite il playground
assistant_id = os.getenv("ASSISTANT_ID")

# Funzione di esempio per utilizzare l'assistant
# def get_assistant_response(prompt):
#     try:
#         response = openai.Assistant.get(assistant_id, input=prompt)
#         print(response)  # Mostra la risposta
#         return response

#     except Exception as e:
#         print(f"Errore durante l'esecuzione: {e}")
