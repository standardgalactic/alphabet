#!/usr/bin/python3

import os
import sys
import fitz  # PyMuPDF

def extract_text_from_pdfs(directory):
    """Extracts text from all PDFs in the given directory."""
    for filename in os.listdir(directory):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(directory, filename)
            process_pdf(pdf_path)

def process_pdf(pdf_path):
    """Extracts text from a single PDF file and saves it as a .txt file."""
    if not os.path.isfile(pdf_path):
        print(f"Error: File not found - {pdf_path}")
        return
    
    text = extract_text_from_pdf(pdf_path)
    if not text.strip():
        print(f"Warning: No text extracted from {pdf_path}")
        return
    
    output_file = f"{pdf_path}.txt"
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Extracted text saved to: {output_file}")
    except Exception as e:
        print(f"Error saving text file for {pdf_path}: {e}")

def extract_text_from_pdf(pdf_path):
    """Extracts text from a single PDF file."""
    text = ""
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            text += page.get_text("text") + "\n"
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
    return text

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "*.pdf":
            extract_text_from_pdfs(os.getcwd())
        else:
            for pdf_file in sys.argv[1:]:
                process_pdf(pdf_file)
    else:
        extract_text_from_pdfs(os.getcwd())