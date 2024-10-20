from flask import Flask, request, jsonify
import pytesseract
from pdf2image import convert_from_path
from PyPDF2 import PdfReader
from fpdf import FPDF
import os

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
    data = request.json  # Legge la richiesta JSON

    # Assicurati che ci sia un file_path
    if not data or 'file_path' not in data:
        return jsonify({'status': 'error', 'message': 'file_path is required'}), 400
    
    file_path = data.get('file_path')  # Ottiene il percorso del file dal JSON

    # Verifica che il file esista
    if not os.path.exists(file_path):
        return jsonify({'status': 'error', 'message': 'File not found'}), 404

    # Controlla se il PDF è leggibile
    if is_pdf_readable(file_path):
        return jsonify({
            'status': 'success',
            'message': 'PDF is readable',
            'file_path': file_path
        })
    
    # Se non è leggibile, esegui la conversione tramite OCR
    output_file_path = os.path.splitext(file_path)[0] + '_converted.pdf'
    convert_pdf_to_text_via_ocr(file_path, output_file_path)

    # Restituisci la risposta con il file convertito
    return jsonify({
        'status': 'success',
        'message': 'PDF was not readable, converted via OCR',
        'converted_file': output_file_path
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
