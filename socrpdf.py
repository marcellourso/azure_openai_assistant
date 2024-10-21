import os
import fitz  # PyMuPDF per controllare se il PDF è leggibile
from flask import Flask, request, jsonify, send_file
import ocrmypdf

app = Flask(__name__)

# Imposta il percorso di default (locale) per i file salvati
DEFAULT_SAVE_PATH = '/tmp'

# Funzione per controllare se il PDF è già leggibile
def is_pdf_readable(file_path):
    try:
        doc = fitz.open(file_path)
        for page_num in range(min(3, doc.page_count)):  # Controlla le prime 3 pagine
            page = doc.load_page(page_num)
            text = page.get_text("text")  # Estrae il testo
            if text.strip():  # Verifica se c'è del testo
                return True
    except Exception as e:
        print(f"Errore durante la verifica del PDF con fitz: {e}")
    
    return False

# Funzione che esegue OCR e salva il PDF convertito
def ocr_pdf(input_file, output_file):
    try:
        print(f"Eseguo OCR su {input_file} e salvo il risultato in {output_file}")
        ocrmypdf.ocr(input_file, output_file)
        print(f"Conversione completata. File salvato in: {output_file}")
        return output_file
    except Exception as e:
        print(f"Errore durante la conversione OCR: {e}")
        return None

# Aggiungi una route per visualizzare il form HTML per il caricamento del file
@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Upload PDF for OCR</title>
    </head>
    <body>
        <h1>Upload a PDF for OCR conversion</h1>
        <form action="/upload" method="POST" enctype="multipart/form-data">
            <input type="file" name="file" required />
            <button type="submit">Upload</button>
        </form>
    </body>
    </html>
    '''

# Endpoint per il caricamento dei file
@app.route('/upload', methods=['POST'])
def upload_file():
    save_path = DEFAULT_SAVE_PATH

    # Controlla se il file è stato caricato
    if 'file' not in request.files:
        return jsonify({'status': 'error', 'message': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'status': 'error', 'message': 'No selected file'}), 400

    if file:
        # Salva il file PDF caricato
        input_file_path = os.path.join(save_path, file.filename)
        file.save(input_file_path)

        # Verifica se il PDF è già leggibile
        if is_pdf_readable(input_file_path):
            # Il PDF è già leggibile, restituisci il file originale senza OCR
            print(f"Il PDF {file.filename} è già leggibile, nessun OCR necessario.")
            return send_file(input_file_path, as_attachment=True)

        # Se non è leggibile, esegui OCR e salva il file di output
        output_file_path = os.path.join(save_path, f"ocr_{file.filename}")
        result_file = ocr_pdf(input_file_path, output_file_path)
        if result_file:
            # Invia il file PDF convertito all'utente
            return send_file(result_file, as_attachment=True)
        else:
            return jsonify({'status': 'error', 'message': 'Error during OCR conversion'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
