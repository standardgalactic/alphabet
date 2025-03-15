#!/usr/bin/python3

import os
import sys
import fitz  # PyMuPDF
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

def extract_text_from_pdfs_and_epubs(directory):
    """Extracts text from all PDFs and EPUBs in the given directory."""
    for filename in os.listdir(directory):
        if filename.lower().endswith(".pdf"):
            file_path = os.path.join(directory, filename)
            process_pdf(file_path)
        elif filename.lower().endswith(".epub"):
            file_path = os.path.join(directory, filename)
            process_epub(file_path)

def process_pdf(pdf_path):
    """Extracts text from a single PDF file and saves it as a .txt file."""
    if not os.path.isfile(pdf_path):
        print(f"Error: File not found - {pdf_path}")
        return
    
    text = extract_text_from_pdf(pdf_path)
    if not text.strip():
        print(f"Warning: No text extracted from {pdf_path}")
        return
    
    output_file = pdf_path.rsplit(".", 1)[0] + ".txt"
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

def process_epub(epub_path):
    """Extracts text from a single EPUB file and saves it as a .txt file."""
    if not os.path.isfile(epub_path):
        print(f"Error: File not found - {epub_path}")
        return
    
    text = extract_text_from_epub(epub_path)
    if not text.strip():
        print(f"Warning: No text extracted from {epub_path}")
        return
    
    output_file = epub_path.rsplit(".", 1)[0] + ".txt"
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Extracted text saved to: {output_file}")
    except Exception as e:
        print(f"Error saving text file for {epub_path}: {e}")

def extract_text_from_epub(epub_path):
    """Extracts text from an EPUB file."""
    text = ""
    try:
        book = epub.read_epub(epub_path)
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                soup = BeautifulSoup(item.get_content(), "html.parser")
                text += soup.get_text() + "\n"
    except Exception as e:
        print(f"Error extracting text from {epub_path}: {e}")
    return text

if __name__ == "__main__":
    if len(sys.argv) > 1:
        for file in sys.argv[1:]:
            if file.lower().endswith(".pdf"):
                process_pdf(file)
            elif file.lower().endswith(".epub"):
                process_epub(file)
            else:
                print(f"Unsupported file type: {file}")
    else:
        extract_text_from_pdfs_and_epubs(os.getcwd())