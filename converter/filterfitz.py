import os
import pytesseract
from flask import Flask, request, jsonify, render_template
import fitz  # PyMuPDF
from fpdf import FPDF

app = Flask(__name__)

# Imposta il percorso di default (locale) per i file salvati
DEFAULT_SAVE_PATH = '/tmp'

# Funzione che verifica se il PDF è leggibile (cioè contiene testo)
def is_pdf_readable(file_path):
    try:
        doc = fitz.open(file_path)
        for page_num in range(min(3, doc.page_count)):  # Controlla le prime 3 pagine
            page = doc.load_page(page_num)
            text = page.get_text("text")  # Estrae il testo
            if text.strip():  # Verifica se c'è del testo
                return True
    except Exception as e:
        print(f"Errore durante la lettura del PDF con fitz: {e}")
    
    return False

# Funzione per convertire PDF tramite OCR in caso non sia leggibile
def convert_pdf_to_text_via_ocr(file_path, output_path):
    """Converte il PDF in testo tramite OCR e lo salva come PDF leggibile."""
    try:
        # Apre il PDF con PyMuPDF
        doc = fitz.open(file_path)
        
        # Crea un nuovo PDF
        pdf = FPDF()
        
        # Itera su ogni pagina del PDF
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            pix = page.get_pixmap()  # Converte la pagina in immagine
            
            # Salva l'immagine temporaneamente
            img_path = f"/tmp/page_{page_num}.png"
            pix.save(img_path)
            
            # Usa pytesseract per estrarre il testo dall'immagine
            text = pytesseract.image_to_string(img_path)
            print(f"Testo estratto da pagina {page_num}: {text[:100]}...")

            # Aggiungi una nuova pagina al PDF
            pdf.add_page()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.set_font("Arial", size=12)
            
            # Inserisci il testo convertito nella nuova pagina
            pdf.multi_cell(0, 10, text.encode('utf-8', 'replace').decode('utf-8'))
        
        # Salva il nuovo PDF convertito
        pdf.output(output_path)
        print(f"PDF salvato correttamente in {output_path}")
        return output_path

    except Exception as e:
        print(f"Errore durante la conversione OCR con fitz: {e}")
        return None

# Aggiungi una route per visualizzare il form HTML
@app.route('/')
def home():
    return render_template('upload.html')

# Endpoint per il caricamento dei file
@app.route('/upload', methods=['POST'])
def upload_file():
    save_path = request.form.get('save_path', DEFAULT_SAVE_PATH)

    # Controlla se il file è stato caricato
    if 'file' not in request.files:
        return jsonify({'status': 'error', 'message': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'status': 'error', 'message': 'No selected file'}), 400

    if file:
        # Salva il file nella directory specificata
        file_path = os.path.join(save_path, file.filename)
        file.save(file_path)

        # Controlla se il PDF è leggibile
        if is_pdf_readable(file_path):
            return jsonify({'status': 'success', 'message': 'PDF is readable', 'file_path': file_path})
        else:
            # Converti il file in PDF leggibile con OCR
            original_filename = os.path.splitext(file.filename)[0]
            output_path = os.path.join(save_path, f"{original_filename}_converted.pdf")
            result_path = convert_pdf_to_text_via_ocr(file_path, output_path)
            if result_path:
                return jsonify({'status': 'success', 'message': 'PDF was not readable, converted via OCR', 'file_path': result_path})
            else:
                return jsonify({'status': 'error', 'message': 'Error during OCR conversion'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
