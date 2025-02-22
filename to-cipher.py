#!/usr/bin/env python3

# Mapping from lowercase letters (a-z) to Logico-Philosophicus symbols

# How to use:
# python3 to-cipher.py input-text.txt output-cipher.txt

# To decipher:
# python3 decipher.py output-cipher.txt output-text.txt

cipher_map = {
    'a': '+', 'b': '-', 'c': '/', 'd': '\\', 'e': '÷', 'f': '*', 'g': '^', 'h': '∋', 'i': '%', 'j': '∈',
    'k': '∫', 'l': '∉', 'm': '√', 'n': '&', 'o': '!', 'p': '≈', 'q': '<', 'r': '|', 's': '>', 't': '≤',
    'u': '≥', 'v': '=', 'w': '⊣', 'x': '⊢', 'y': '⊥', 'z': '⊤'
}

# Read input file, convert to lowercase, and transliterate to cipher
def to_cipher(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
            for line in infile:
                # Convert to lowercase and replace each letter with its cipher symbol
                cipher_text = ''.join(cipher_map.get(char.lower(), char) for char in line)
                outfile.write(cipher_text)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python to_cipher.py input.txt output_cipher.txt")
        sys.exit(1)
    to_cipher(sys.argv[1], sys.argv[2])