import os
import fitz  # PyMuPDF

PDF_FOLDER = "pdfs"

# Function to extract text from PDFs
def extract_text(pdf_folder):
    filenames, texts = [], []
    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            doc = fitz.open(os.path.join(pdf_folder, filename))
            text = "\n".join(page.get_text() for page in doc)
            texts.append(text)
            filenames.append(filename)
    return filenames, texts

# Extract text from PDFs
filenames, documents = extract_text(PDF_FOLDER)
