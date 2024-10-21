import os
import fitz  # PyMuPDF
import ocrmypdf
import shutil

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
        print(f"Errore durante la conversione OCR per {input_file}: {e}")

# Funzione principale per analizzare la cartella e creare una versione leggibile dei file
def process_folder(root_folder):
    # Crea il nome della nuova cartella con suffisso "_readable"
    readable_folder = f"{root_folder}_readable"
    
    # Scansione ricorsiva della cartella originale
    for foldername, subfolders, filenames in os.walk(root_folder):
        # Ricrea la struttura della cartella nella nuova cartella "_readable"
        relative_path = os.path.relpath(foldername, root_folder)
        new_folder_path = os.path.join(readable_folder, relative_path)
        os.makedirs(new_folder_path, exist_ok=True)

        # Scansiona tutti i file nella cartella corrente
        for filename in filenames:
            if filename.lower().endswith('.pdf'):
                original_file_path = os.path.join(foldername, filename)
                new_file_path = os.path.join(new_folder_path, filename)

                if is_pdf_readable(original_file_path):
                    print(f"{filename} è già leggibile, copiato senza modifiche.")
                    shutil.copyfile(original_file_path, new_file_path)  # Copia il file leggibile senza modificarlo
                else:
                    print(f"{filename} non è leggibile, avvio conversione OCR.")
                    convert_pdf_to_readable(original_file_path, new_file_path)  # Converte il file con OCR

    print(f"Tutti i file sono stati processati e salvati in {readable_folder}")

# Esempio di esecuzione:
if __name__ == "__main__":
    # Sostituisci questo percorso con il percorso alla tua cartella radice
    root_folder = "/home/marcello/Documents/SOBA_dued"
    
    process_folder(root_folder)
