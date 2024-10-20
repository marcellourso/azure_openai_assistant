import os
import pytesseract
from flask import Flask, request, jsonify
from PyPDF2 import PdfFileReader
from pdf2image import convert_from_path
from fpdf import FPDF

app = Flask(__name__)

# Imposta il percorso di default (locale) per i file salvati
DEFAULT_SAVE_PATH = '/tmp'

def is_pdf_readable(file_path):
    
    try:
        with open(file_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            # Estrarre testo dalle prime pagine (puoi regolare quante pagine verificare)
            for page_num in range(min(3, len(reader.pages))):  # Limitiamo alle prime 3 pagine per velocità
                page = reader.pages[page_num]
                text = page.extract_text()
                if text and 'a' in text.lower():  # Controlla se 'a' è presente nel testo
                    return True
    except Exception as e:
        print(f"Errore durante la lettura del PDF: {e}")
    
    return False

def convert_pdf_to_text_via_ocr(file_path, output_path):
    """Converte il PDF in testo tramite OCR e lo salva come PDF."""
    # Converte le pagine PDF in immagini
    images = convert_from_path(file_path)
    
    # Crea un nuovo PDF
    pdf = FPDF()
    
    for img in images:
        text = pytesseract.image_to_string(img)  # OCR sull'immagine
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)
        # pdf.multi_cell(0, 10, text)
        pdf.multi_cell(0, 10, text.encode('latin-1', 'replace').decode('latin-1'))
    
    # Salva il nuovo PDF
    pdf.output(output_path)
    return output_path

@app.route('/upload', methods=['POST'])
def upload_file():
    save_path = request.form.get('save_path', DEFAULT_SAVE_PATH)

    # Controlla se il file è stato caricato
    if 'file' not in request.files:
        return jsonify({'status': 'error', 'message': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'status': 'error', 'message': 'No selected file'})

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
            convert_pdf_to_text_via_ocr(file_path, output_path)
            return jsonify({'status': 'success', 'message': 'PDF was not readable, converted via OCR', 'file_path': output_path})

if __name__ == '__main__':
    app.run(debug=True)
