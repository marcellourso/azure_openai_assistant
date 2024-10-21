import ocrmypdf

def ocr_pdf(input_file, output_file):
    try:
        # Esegui OCR sul PDF
        print(f"Eseguo OCR su {input_file} e salvo il risultato in {output_file}")
        ocrmypdf.ocr(input_file, output_file)
        print(f"Conversione completata. File salvato in: {output_file}")
    except Exception as e:
        print(f"Errore durante la conversione OCR: {e}")

# Specifica il file di input e il file di output
input_pdf = "pignoramento.pdf"  # Sostituisci con il percorso al tuo PDF di input
output_pdf = "output.pdf"  # Sostituisci con il percorso al PDF di output

# Esegui la funzione di conversione OCR
ocr_pdf(input_pdf, output_pdf)
