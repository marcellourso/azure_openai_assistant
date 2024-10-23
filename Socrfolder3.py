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
        print(f"Avvio conversione OCR per {input_file}")
        ocrmypdf.ocr(input_file, output_file)
        print(f"Convertito {input_file} in {output_file}")
    except Exception as e:
        print(f"Errore durante la conversione OCR per {input_file}: {e}")

# Funzione principale per scorrere la cartella e processare i PDF
def process_folder(root_folder):
    print(f"Inizio elaborazione della cartella: {root_folder}")
    
    # Crea il nome della nuova cartella con suffisso "_readable"
    readable_folder = f"{root_folder}_readable"
    os.makedirs(readable_folder, exist_ok=True)
    print(f"Creata la cartella destinazione: {readable_folder}")

    for foldername, subfolders, filenames in os.walk(root_folder):
        print(f"Scansione della cartella: {foldername}")
        
        for filename in filenames:
            original_file_path = os.path.join(foldername, filename)
            print(f"File trovato: {filename}")

            # Se è un file PDF, esegui il controllo e la conversione OCR
            if filename.lower().endswith('.pdf'):
                new_file_path = os.path.join(readable_folder, filename)

                if is_pdf_readable(original_file_path):
                    print(f"{filename} è già leggibile, copiato senza modifiche.")
                    shutil.copyfile(original_file_path, new_file_path)  # Copia il file leggibile senza modificarlo
                else:
                    print(f"{filename} non è leggibile, avvio conversione OCR.")
                    convert_pdf_to_readable(original_file_path, new_file_path)  # Converte il file con OCR
            else:
                print(f"{filename} non è un PDF, saltato.")

    return readable_folder

# Endpoint per caricare la pagina HTML
@app.route('/')
def home():
    return render_template('index.html')

# Endpoint per ricevere il percorso della cartella e processare i file PDF
@app.route('/process_folder', methods=['POST'])
def process_folder_endpoint():
    root_folder = request.form.get('folder')
    if not root_folder or not os.path.exists(root_folder):
        print(f"Errore: cartella non valida - {root_folder}")
        return jsonify({'error': 'Cartella non valida o inesistente'}), 400

    print(f"Percorso cartella ricevuto: {root_folder}")
    result_folder = process_folder(root_folder)
    print(f"Processo completato. Cartella destinazione: {result_folder}")
    
    return jsonify({'message': f'Tutti i file sono stati processati e salvati in {result_folder}'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
