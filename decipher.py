#!/usr/bin/env python3

# Reverse mapping from Logico-Philosophicus cipher symbols to lowercase letters

# How to use:
# python3 to-cipher.py input-text.txt output-cipher.txt

# To decipher:
# python3 decipher.py output-cipher.txt output-text.txt

reverse_cipher_map = {
    '+': 'a', '-': 'b', '/': 'c', '\\': 'd', '÷': 'e', '*': 'f', '^': 'g', '∋': 'h', '%': 'i', '∈': 'j',
    '∫': 'k', '∉': 'l', '√': 'm', '&': 'n', '!': 'o', '≈': 'p', '<': 'q', '|': 'r', '>': 's', '≤': 't',
    '≥': 'u', '=': 'v', '⊣': 'w', '⊢': 'x', '⊥': 'y', '⊤': 'z'
}

# Read cipher file and convert back to lowercase text
def from_cipher(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
            for line in infile:
                # Replace each symbol with its corresponding letter, keeping non-mapped chars
                text = ''.join(reverse_cipher_map.get(char, char) for char in line)
                outfile.write(text)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python from_cipher.py input-cipher.txt output-text.txt")
        sys.exit(1)
    from_cipher(sys.argv[1], sys.argv[2])