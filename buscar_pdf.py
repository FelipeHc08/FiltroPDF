import PyPDF2
import re
import shutil
import os
import glob
import tkinter as tk
from tkinter import ttk, filedialog
from ttkthemes import ThemedStyle

def extract_text_from_pdf(pdf_file: str) -> [str]:
    with open(pdf_file, 'rb') as pdf:
        reader = PyPDF2.PdfReader(pdf)
        pdf_text = []

        for page in reader.pages:
            content = page.extract_text()
            pdf_text.append(content)

        return pdf_text

def move_pdfs(pdf_folder, destination_folder, completion_label, filter_word):
    # Garantir que as pastas existam
    if not os.path.exists(pdf_folder):
        print(f"A pasta de origem '{pdf_folder}' não existe.")
        return

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Obter lista de arquivos PDF na pasta
    pdf_files = glob.glob(os.path.join(pdf_folder, '*.pdf'))

    for pdf_file_path in pdf_files:
        extracted_text = extract_text_from_pdf(pdf_file_path)
        teste_count = 0

        for text in extracted_text:
            split_message = re.split(r'\s+|[,;?!.-]\s*', text.lower())

            if filter_word.lower() in split_message:
                teste_count += 1
                print(f"A palavra {filter_word} apareceu no arquivo {os.path.basename(pdf_file_path)}:", teste_count)

                # Mover o arquivo para a pasta de destino
                destination_path = os.path.join(destination_folder, os.path.basename(pdf_file_path))
                shutil.move(pdf_file_path, destination_path)

                print(f"Arquivo movido para {destination_folder}")

    # Atualizar a etiqueta de conclusão
    completion_label.config(text="Execução concluída")

def browse_pdf_folder():
    folder_path = filedialog.askdirectory()
    pdf_folder_entry.delete(0, tk.END)
    pdf_folder_entry.insert(0, folder_path)

def browse_destination_folder():
    folder_path = filedialog.askdirectory()
    destination_folder_entry.delete(0, tk.END)
    destination_folder_entry.insert(0, folder_path)

def execute_program():
    pdf_folder = pdf_folder_entry.get()
    destination_folder = destination_folder_entry.get()
    filter_word = filter_entry.get()

    # Criar e exibir etiqueta de execução
    completion_label = ttk.Label(root, text="")
    completion_label.pack(pady=5)

    # Mover arquivos e atualizar etiqueta de conclusão
    move_pdfs(pdf_folder, destination_folder, completion_label, filter_word)

# Interface gráfica com Tkinter
root = tk.Tk()
root.title("Organizador de PDF V0.1")

# Configurar a geometria da janela para um tamanho maior
root.geometry("600x400")

# Aplicar estilo temático
style = ThemedStyle(root)
style.set_theme("equilux")

# Título centralizado
tk.Label(root, text="Organizador de PDF V0.1", font=("Helvetica", 16)).pack(pady=10)
# Entrada para a pasta de origem
tk.Label(root, text="Pasta de Origem:").pack()
pdf_folder_entry = ttk.Entry(root)
pdf_folder_entry.pack(pady=5)
ttk.Button(root, text="Procurar", command=browse_pdf_folder).pack(pady=5)

# Entrada para a pasta de destino
tk.Label(root, text="Pasta de Destino:").pack()
destination_folder_entry = ttk.Entry(root)
destination_folder_entry.pack(pady=5)
ttk.Button(root, text="Procurar", command=browse_destination_folder).pack(pady=5)

# Entrada para a palavra de filtro
tk.Label(root, text="Palavra de Filtro:").pack()
filter_entry = ttk.Entry(root)
filter_entry.pack(pady=5)

# Botão para executar o programa
ttk.Button(root, text="Executar", command=execute_program).pack(pady=10)

root.mainloop()
