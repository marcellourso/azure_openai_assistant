# Usa l'immagine base di Python
FROM python:3.9-slim

# Installiamo tutte le dipendenze necessarie
RUN apt-get update && apt-get install -y \
    libsm6 libxext6 libxrender-dev \
    tesseract-ocr tesseract-ocr-eng \
    poppler-utils && \
    rm -rf /var/lib/apt/lists/*

# Creiamo una directory di lavoro
WORKDIR /app

# Copiamo il file di requirements e installiamo le dipendenze Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamo tutto il contenuto nel container
COPY . .

# Esponiamo la porta 5000 per Flask
EXPOSE 5000

# Comando per avviare l'applicazione Flask
CMD ["python", "filterfitz.py"]
