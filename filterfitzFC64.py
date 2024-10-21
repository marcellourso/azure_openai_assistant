import os
import pytesseract
from flask import Flask, request, jsonify
from pdf2image import convert_from_path
from PyPDF2 import PdfReader
from fpdf import FPDF

app = Flask(__name__)

# Percorso di default per il salvataggio dei file
DEFAULT_SAVE_PATH = '/tmp'

# Funzione per controllare se il PDF è leggibile
def is_pdf_readable(file_path):
    try:
        with open(file_path, 'rb') as pdf_file:
            reader = PdfReader(pdf_file)
            for page_num in range(min(3, len(reader.pages))):
                page = reader.pages[page_num]
                text = page.extract_text()
                if text and 'a' in text.lower():
                    return True
    except Exception as e:
        print(f"Errore durante la lettura del PDF: {e}")
    return False

# Funzione per convertire il PDF tramite OCR e creare un nuovo PDF leggibile
def convert_pdf_to_text_via_ocr(file_path, output_path):
    images = convert_from_path(file_path)
    pdf = FPDF()
    for img in images:
        text = pytesseract.image_to_string(img)
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, text.encode('latin-1', 'replace').decode('latin-1'))
    pdf.output(output_path)
    return output_path

# Endpoint per gestire la chiamata della function via API
@app.route('/function_call', methods=['POST'])
def function_call():
    # Controlla se il file è stato caricato
    if 'file' not in request.files:
        return jsonify({'status': 'error', 'message': 'No file part'})

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'status': 'error', 'message': 'No selected file'})
    
    # Salva il file nella directory temporanea
    save_path = DEFAULT_SAVE_PATH
    file_full_path = os.path.join(save_path, file.filename)
    file.save(file_full_path)

    # Verifica se il PDF è leggibile
    if is_pdf_readable(file_full_path):
        return jsonify({
            'status': 'success',
            'message': 'PDF is readable',
            'file_path': file_full_path
        })
    
    # Se non è leggibile, esegui la conversione tramite OCR
    output_file_path = os.path.splitext(file_full_path)[0] + '_converted.pdf'
    convert_pdf_to_text_via_ocr(file_full_path, output_file_path)

    # Restituisci la risposta con il file convertito
    return jsonify({
        'status': 'success',
        'message': 'PDF was not readable, converted via OCR',
        'converted_file': output_file_path
    })

if __name__ == '__main__':
    app.run(debug=True)
