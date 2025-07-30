import os
import fitz  # PyMuPDF

PDF_FOLDER = "pdfs"

# Function to extract text from PDFs
def extract_text(pdf_folder):
    filenames, documents = [], []
    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            document = fitz.open(os.path.join(pdf_folder, filename))
            text = "\n".join(page.get_text() for page in document)
            documents.append(text)
            filenames.append(filename)
    return filenames, documents
