#!/usr/bin/env python3
"""
A script to extract plain text from all MHTML files in the current directory.
It parses each MHTML file as a MIME message, extracts text from its HTML (or plain text) parts,
removes tags using BeautifulSoup, and writes the results to separate .txt files.

Usage: 
    python extract_mhtml_text.py

Ensure you have installed BeautifulSoup (e.g., pip install beautifulsoup4)
"""

import glob
import os
from email import policy
from email.parser import BytesParser
from bs4 import BeautifulSoup

def extract_text_from_mhtml(file_path):
    """
    Extract plain text from an MHTML file by parsing its MIME structure.
    It processes both HTML parts (removing tags) and plain text parts.
    """
    with open(file_path, 'rb') as f:
        msg = BytesParser(policy=policy.default).parse(f)
    
    text_parts = []

    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            # Process HTML content by removing HTML tags
            if content_type == 'text/html':
                html_content = part.get_content()
                soup = BeautifulSoup(html_content, 'html.parser')
                text_parts.append(soup.get_text(separator="\n", strip=True))
            # If plain text is available, extract it as well
            elif content_type == 'text/plain':
                text_parts.append(part.get_content())
    else:
        content_type = msg.get_content_type()
        if content_type == 'text/html':
            soup = BeautifulSoup(msg.get_content(), 'html.parser')
            text_parts.append(soup.get_text(separator="\n", strip=True))
        else:
            text_parts.append(msg.get_content())
    
    return "\n\n".join(text_parts)

def main():
    # Find all .mhtml files in the current directory
    mhtml_files = glob.glob("*.mhtml")
    if not mhtml_files:
        print("No MHTML files found in the current directory.")
        return
    
    for file_path in mhtml_files:
        print(f'Processing {file_path} ...')
        extracted_text = extract_text_from_mhtml(file_path)
        output_file = os.path.splitext(file_path)[0] + ".txt"
        with open(output_file, "w", encoding="utf-8") as out:
            out.write(extracted_text)
        print(f"Extracted text written to {output_file}")

if __name__ == "__main__":
    main()
