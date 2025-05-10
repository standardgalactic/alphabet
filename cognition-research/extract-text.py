#!/usr/bin/env python3
"""
A script to extract plain text from PDF, EPUB, and MHTML files.

It can process specific files passed as arguments, or scan the current directory.

Usage:
    python extract_text.py file1.pdf file2.epub
    python extract_text.py                 # processes all PDF, EPUB, and MHTML in current dir

Dependencies:
    pip install PyMuPDF ebooklib beautifulsoup4
"""

import os
import sys
import fitz  # PyMuPDF
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
from email import policy
from email.parser import BytesParser

def normalize_quotes(text):
    """Replace smart quotes, dashes, and other problematic characters."""
    replacements = {
        "\u2018": "'", "\u2019": "'",  # Single quotes
        "\u201c": '"', "\u201d": '"',  # Double quotes
        "\u2014": "—", "\u2013": "-",  # Dashes
        "\u2026": "...", "\u00a0": " "  # Ellipsis, non-breaking space
    }
    for smart, plain in replacements.items():
        text = text.replace(smart, plain)
    return text

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            text += page.get_text("text") + "\n"
    except Exception as e:
        print(f"[!] Error extracting text from {pdf_path}: {e}")
    return normalize_quotes(text)

def extract_text_from_epub(epub_path):
    text = ""
    try:
        book = epub.read_epub(epub_path)
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                soup = BeautifulSoup(item.get_content(), "html.parser")
                text += soup.get_text() + "\n"
    except Exception as e:
        print(f"[!] Error extracting text from {epub_path}: {e}")
    return normalize_quotes(text)

def extract_text_from_mhtml(mhtml_path):
    text_parts = []
    try:
        with open(mhtml_path, 'rb') as f:
            msg = BytesParser(policy=policy.default).parse(f)

        def decode_part(part):
            charset = part.get_content_charset() or 'utf-8'
            try:
                return part.get_payload(decode=True).decode(charset, errors='replace')
            except Exception as e:
                print(f"[!] Decode error in {mhtml_path}: {e}")
                return ''

        if msg.is_multipart():
            for part in msg.walk():
                ctype = part.get_content_type()
                if ctype == 'text/html':
                    html = decode_part(part)
                    soup = BeautifulSoup(html, 'html.parser')
                    text_parts.append(soup.get_text(separator="\n", strip=True))
                elif ctype == 'text/plain':
                    text_parts.append(decode_part(part))
        else:
            content = decode_part(msg)
            ctype = msg.get_content_type()
            if ctype == 'text/html':
                soup = BeautifulSoup(content, 'html.parser')
                text_parts.append(soup.get_text(separator="\n", strip=True))
            else:
                text_parts.append(content)
    except Exception as e:
        print(f"[!] Error reading MHTML {mhtml_path}: {e}")
    
    return normalize_quotes("\n\n".join(text_parts))

def save_text(text, original_path):
    output_file = os.path.splitext(original_path)[0] + ".txt"
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"[✓] Text saved to: {output_file}")
    except Exception as e:
        print(f"[!] Error writing to {output_file}: {e}")

def process_file(file_path):
    if not os.path.isfile(file_path):
        print(f"[!] File not found: {file_path}")
        return

    ext = file_path.lower()
    print(f"[•] Processing {file_path}...")
    
    if ext.endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    elif ext.endswith(".epub"):
        text = extract_text_from_epub(file_path)
    elif ext.endswith((".mhtml", ".mht")):
        text = extract_text_from_mhtml(file_path)
    else:
        print(f"[!] Unsupported file type: {file_path}")
        return

    if text.strip():
        save_text(text, file_path)
    else:
        print(f"[!] No text extracted from: {file_path}")

def process_directory(directory):
    for filename in os.listdir(directory):
        if filename.lower().endswith((".pdf", ".epub", ".mhtml", ".mht")):
            process_file(os.path.join(directory, filename))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        for file in sys.argv[1:]:
            process_file(file)
    else:
        print("[i] No files specified. Processing current directory...")
        process_directory(os.getcwd())

