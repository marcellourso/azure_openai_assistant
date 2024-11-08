CODICE PER CARICARE ED INDICIZZARE FILE NEL BLOB STORAGE SUL THREAD CORRENTE

import os
from azure.storage.blob import BlobServiceClient
import openai
import requests

# Configura i client
blob_service_client = BlobServiceClient.from_connection_string("AZURE_STORAGE_CONNECTION_STRING")
container_name = "assistant-files"
search_endpoint = "AZURE_AI_SEARCH_ENDPOINT"
search_api_key = "AZURE_AI_SEARCH_API_KEY"
index_name = "AZURE_AI_SEARCH_INDEX_NAME"

# Funzione per caricare un file su Blob Storage
def upload_file_to_blob(file_path, blob_name):
    container_client = blob_service_client.get_container_client(container_name)
    with open(file_path, "rb") as data:
        container_client.upload_blob(name=blob_name, data=data, overwrite=True)

# Funzione per indicizzare un documento in Azure AI Search
def index_document_in_ai_search(document):
    headers = {
        "Content-Type": "application/json",
        "api-key": search_api_key
    }
    response = requests.post(f"{search_endpoint}/indexes/{index_name}/docs/index", headers=headers, json=document)
    response.raise_for_status()

# Funzione per iterare su tutti i file in una cartella e caricarli
def process_folder(folder_path, thread_id, categoria=None):
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_id = f"{thread_id}_{file_name}"
            
            # Carica il file in Blob Storage con struttura `thread_id/categoria/file_id`
            if categoria:
                blob_name = f"{thread_id}/{categoria}/{file_id}"
            else:
                blob_name = f"{thread_id}/{file_id}"
            
            upload_file_to_blob(file_path, blob_name)
            
            # Crea il documento per Azure AI Search
            document = {
                "id": file_id,
                "thread_id": thread_id,
                "categoria": categoria or "default",  # Imposta la categoria se specificata
                "file_name": file_name,
                "content": "Contenuto estratto o anteprima",
                "created_at": "2024-01-01T00:00:00Z"
            }
            index_document_in_ai_search(document)

            # (Opzionale) Genera embedding e aggiungi al vector store
            embedding = openai.Embedding.create(input=document["content"], model="text-embedding-ada-002")
            add_embedding_to_vector_store(embedding, file_id)  # Pseudo-funzione per aggiungere embedding

# Esempio di utilizzo
process_folder("path/to/your/folder", thread_id="thread_123", categoria="bilanci")
