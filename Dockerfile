# Usa un'immagine Python come base
FROM python:3.9-slim

# Imposta la directory di lavoro
WORKDIR /app

# Copia i file requirements e installa le dipendenze
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia il codice dell'app
COPY . .

# Esponi la porta su cui Flask sarà eseguito
EXPOSE 5000

# Comando per avviare l'app Flask
CMD ["python3", "Socrfolder2.py"]

