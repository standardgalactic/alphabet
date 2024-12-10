#!/usr/bin/python3

import sys
import re

# Mapping for Unicode Italic letters
italic_map = {
    'A': '𝘈', 'B': '𝘉', 'C': '𝘊', 'D': '𝘋', 'E': '𝘌', 'F': '𝘍', 'G': '𝘎', 'H': '𝘏', 'I': '𝘐', 'J': '𝘑',
    'K': '𝘒', 'L': '𝘓', 'M': '𝘔', 'N': '𝘕', 'O': '𝘖', 'P': '𝘗', 'Q': '𝘘', 'R': '𝘙', 'S': '𝘚', 'T': '𝘛',
    'U': '𝘜', 'V': '𝘝', 'W': '𝘞', 'X': '𝘟', 'Y': '𝘠', 'Z': '𝘡',
    'a': '𝘢', 'b': '𝘣', 'c': '𝘤', 'd': '𝘥', 'e': '𝘦', 'f': '𝘧', 'g': '𝘨', 'h': '𝘩', 'i': '𝘪', 'j': '𝘫',
    'k': '𝘬', 'l': '𝘭', 'm': '𝘮', 'n': '𝘯', 'o': '𝘰', 'p': '𝘱', 'q': '𝘲', 'r': '𝘳', 's': '𝘴', 't': '𝘵',
    'u': '𝘶', 'v': '𝘷', 'w': '𝘸', 'x': '𝘹', 'y': '𝘺', 'z': '𝘻'
}

# Function to convert a string to its Unicode Italic equivalent
def convert_to_italic(text):
    return ''.join(italic_map.get(char, char) for char in text)

# Function to process content between <i></i> tags
def convert_italic_tags(content):
    # Regex to find all <i></i> tags and their content
    def replace_match(match):
        original_text = match.group(1)
        return f"<i>{convert_to_italic(original_text)}</i>"

    # Replace the content inside the <i> tags
    return re.sub(r'<i>(.*?)<\/i>', replace_match, content, flags=re.DOTALL)

# Main function to handle command-line arguments
if __name__ == "__main__":
    # Check if the script received a filename as an argument
    if len(sys.argv) < 2:
        print("Usage: python italicise.py <input-file>")
    else:
        # Get the input file from command-line arguments
        input_file = sys.argv[1]

        try:
            # Read the original file
            with open(input_file, 'r', encoding='utf-8') as file:
                content = file.read()

            # Convert only the text between <i></i> tags to Unicode Italic
            new_content = convert_italic_tags(content)

            # Output the new content to stdout (for redirecting or capturing in Vim)
            print(new_content)

        except Exception as e:
            print(f"An error occurred: {e}", file=sys.stderr)
