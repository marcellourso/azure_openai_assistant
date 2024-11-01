import os
import fitz  # PyMuPDF
import ocrmypdf
import shutil
import tkinter as tk
import datetime
import sys
from tkinter import messagebox
from tkinter import filedialog, messagebox

# Funzioni OCR per verificare e convertire i PDF
def is_pdf_readable(file_path):
    try:
        doc = fitz.open(file_path)
        for page_num in range(min(3, doc.page_count)):
            page = doc.load_page(page_num)
            text = page.get_text("text")
            if text.strip():
                return True
    except Exception as e:
        print(f"Errore durante la verifica del PDF con fitz: {e}")
    return False

def convert_pdf_to_readable(input_file, output_file):
    try:
        ocrmypdf.ocr(input_file, output_file)
        print(f"Convertito {input_file} in {output_file}")
    except Exception as e:
        if "Tagged PDF" in str(e):
            print(f"{input_file} è già un PDF taggato e non necessita di OCR. Saltato.")
        else:
            print(f"Errore durante la conversione OCR per {input_file}: {e}")
            raise

def process_folder(root_folder, status_label, select_button, process_button):
    readable_folder = f"{root_folder}_readable"
    try:
        for foldername, subfolders, filenames in os.walk(root_folder):
            relative_path = os.path.relpath(foldername, root_folder)
            new_folder_path = os.path.join(readable_folder, relative_path)
            os.makedirs(new_folder_path, exist_ok=True)

            for filename in filenames:
                original_file_path = os.path.join(foldername, filename)
                new_file_path = os.path.join(new_folder_path, filename)

                if filename.lower().endswith('.pdf'):
                    if is_pdf_readable(original_file_path):
                        print(f"{filename} è già leggibile, copiato senza modifiche.")
                        shutil.copyfile(original_file_path, new_file_path)
                    else:
                        print(f"{filename} non è leggibile, avvio conversione OCR.")
                        convert_pdf_to_readable(original_file_path, new_file_path)
                else:
                    print(f"{filename} non è un PDF, copiato senza modifiche.")
                    shutil.copyfile(original_file_path, new_file_path)

        status_label.config(text="Processo completato!")
        messagebox.showinfo("Completato", f"I file sono stati processati correttamente in {readable_folder}")
    except Exception as e:
        status_label.config(text="Errore irreversibile durante l'elaborazione")
        print(f"Errore durante l'elaborazione della cartella {root_folder}: {e}")
    finally:
        # Riabilita i pulsanti alla fine del processo
        select_button.config(state=tk.NORMAL)
        process_button.config(state=tk.NORMAL)

# Configurazione della GUI con Tkinter
def start_gui():
    root = tk.Tk()
    root.title("conversioni PDF per la lettura")
    root.geometry("400x200")
    root.configure(bg='#f4f4f4')

    def select_folder():
        folder_selected = filedialog.askdirectory()
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, folder_selected)

    def start_processing():
        root_folder = folder_entry.get()
        if not root_folder or not os.path.exists(root_folder):
            messagebox.showerror("Errore", "Seleziona una cartella valida.")
            return

        # Disabilita i pulsanti per evitare altre azioni durante l'elaborazione
        select_button.config(state=tk.DISABLED)
        process_button.config(state=tk.DISABLED)

        status_label.config(text="Lavoro in corso...")
        root.update()  # Aggiorna l'interfaccia per mostrare il messaggio di stato
        process_folder(root_folder, status_label, select_button, process_button)

    # Componenti dell'interfaccia
    tk.Label(root, text="Percorso cartella:", bg='#f4f4f4').pack(pady=10)
    folder_entry = tk.Entry(root, width=40)
    folder_entry.pack()

    select_button = tk.Button(root, text="Seleziona Cartella", command=select_folder)
    select_button.pack(pady=5)

    process_button = tk.Button(root, text="Avvia Processo", command=start_processing, bg="#28a745", fg="white")
    process_button.pack(pady=10)

    status_label = tk.Label(root, text="Stato del processo: In attesa...", bg='#f4f4f4')
    status_label.pack(pady=10)

    root.mainloop()

# Verifica della data limite
def check_date_limit():
    date_limit = datetime.date(2024, 12, 25)
    today = datetime.date.today()
    if today > date_limit:
        # Mostra un messaggio di errore e termina l'applicazione
        messagebox.showerror("Errore", "L'applicazione è scaduta e non è più utilizzabile.")
        sys.exit()

# Avvio dell'interfaccia Tkinter
if __name__ == "__main__":
    check_date_limit()  # Controllo della data limite prima di avviare l'interfaccia
    start_gui()         # Avvio dell'interfaccia solo se la data limite non è stata superata
