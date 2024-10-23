import os
import fitz  # PyMuPDF
import ocrmypdf
import shutil
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

# Funzione per verificare se il PDF è leggibile
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

# Funzione per eseguire l'OCR e salvare il PDF leggibile
def convert_pdf_to_readable(input_file, output_file):
    try:
        ocrmypdf.ocr(input_file, output_file)
        print(f"Convertito {input_file} in {output_file}")
    except Exception as e:
        # Gestione specifica per l'errore "Tagged PDF"
        if "Tagged PDF" in str(e):
            print(f"{input_file} è già un PDF taggato e non necessita di OCR. Saltato.")
        else:
            print(f"Errore durante la conversione OCR per {input_file}: {e}")
            raise

# Funzione principale per analizzare la cartella e creare una versione leggibile dei file
def process_folder(root_folder):
    # Crea il nome della nuova cartella con suffisso "_readable"
    readable_folder = f"{root_folder}_readable"
    
    try:
        # Scansione ricorsiva della cartella originale
        for foldername, subfolders, filenames in os.walk(root_folder):
            # Ricrea la struttura della cartella nella nuova cartella "_readable"
            relative_path = os.path.relpath(foldername, root_folder)
            new_folder_path = os.path.join(readable_folder, relative_path)
            os.makedirs(new_folder_path, exist_ok=True)

            # Scansiona tutti i file nella cartella corrente
            for filename in filenames:
                original_file_path = os.path.join(foldername, filename)
                new_file_path = os.path.join(new_folder_path, filename)

                # Se è un file PDF, esegui il controllo e conversione OCR
                if filename.lower().endswith('.pdf'):
                    if is_pdf_readable(original_file_path):
                        print(f"{filename} è già leggibile, copiato senza modifiche.")
                        shutil.copyfile(original_file_path, new_file_path)  # Copia il file leggibile senza modificarlo
                    else:
                        print(f"{filename} non è leggibile, avvio conversione OCR.")
                        convert_pdf_to_readable(original_file_path, new_file_path)  # Converte il file con OCR
                else:
                    # Se non è un PDF, copia il file senza modificarlo
                    print(f"{filename} non è un PDF, copiato senza modifiche.")
                    shutil.copyfile(original_file_path, new_file_path)

        return {'status': 'good working', 'message': f'I file sono stati processati correttamente in {readable_folder}'}
    
    except Exception as e:
        # Se si verifica un errore irreversibile, gestiscilo qui
        print(f"Errore durante l'elaborazione della cartella {root_folder}: {e}")
        return {'status': 'solving problem', 'message': 'Sto risolvendo alcuni problemi...'}

# Route per la pagina principale di caricamento
@app.route('/')
def home():
    return render_template('index.html')

# Route per ricevere la cartella radice e processare i file
@app.route('/process', methods=['POST'])
def process():
    root_folder = request.form.get('folder')
    if not root_folder or not os.path.exists(root_folder):
        return jsonify({'error': 'Cartella non valida'}), 400

    result = process_folder(root_folder)
    
    if result['status'] == 'good working':
        return jsonify({'message': result['message'], 'status': 'processamento in corso...'})
    else:
        return jsonify({'message': result['message'], 'status': 'solving problem, wait...'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
