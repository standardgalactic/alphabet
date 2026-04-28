#!/usr/bin/env bash

set -euo pipefail

LOG_FILE="flyxion_corrections.log"
REPLACEMENT="Flyxion"

TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
BACKUP_DIR="backup_$TIMESTAMP"

echo "Creating backup snapshot: $BACKUP_DIR"
mkdir -p "$BACKUP_DIR"

while IFS= read -r -d '' file; do
    mkdir -p "$BACKUP_DIR/$(dirname "$file")"
    cp "$file" "$BACKUP_DIR/$file"
done < <(find . -type f \( -name "*.json" -o -name "*.srt" -o -name "*.tsv" -o -name "*.txt" -o -name "*.vtt" \) ! -path "./backup_*/*" -print0)

echo "Backup complete."

python3 <<'PY'
import re
import difflib
import pathlib

REPLACEMENT = "Flyxion"
TARGET = "flyxion"
LOG_FILE = "flyxion_corrections.log"

extensions = {".json", ".srt", ".tsv", ".txt", ".vtt"}

KNOWN_VARIANTS = re.compile(
    r'(?i)(?<![A-Za-z])('
    r'Flexion|Flixian|Flixing|Fliction|Flippshen|Flexumian|Fletchian|Flicksheen|'
    r'Flyzion|Flyxen|Flyxian|Flyxionn|Flyxionne|Flykshun|Flykshion|Flikshun|'
    r'Flikzion|Flikxion|Flixion|Fleksion|Fleksian|Flextion|Flicksion|'
    r'Flickzion|Flickxion|Flickshank|Fleksheen|Flekshun|Flekzion|Flixyon|'
    r'Flixxon|Flixionne|Felician|Flyxionu|Flick Sheenan|Flicksheen|'
    r'Flickshian|Flitschian|Flickian|Flixson|Flijnen|Flitian|Flickshan|'
    r'Flickstahn|Flexiton|Flakiron|Flickshahn|Flixie|Flixan|Fugchin|'
    r'Flickshen|Flickshin|Flixgen|Flixen|Flicksham|Flitchinan|Flickening'
    r')(?![A-Za-z])'
)

PROTECTED = {
    "affliction": "__PROTECTED_AFFLICTION__",
    "Affliction": "__PROTECTED_CAP_AFFLICTION__",
    "infliction": "__PROTECTED_INFLICTION__",
    "Infliction": "__PROTECTED_CAP_INFLICTION__",
}

def strip_invisible_chars(text):
    return re.sub(r'[\u200B-\u200D\uFEFF]', '', text)

def protect_real_words(text):
    for word, marker in PROTECTED.items():
        text = re.sub(rf'\b{re.escape(word)}\b', marker, text)
    return text

def restore_real_words(text):
    for word, marker in PROTECTED.items():
        text = text.replace(marker, word)
    return text

def close_to_flyxion(word):
    w = word.lower()

    if w == TARGET:
        return False

    if len(w) < 5 or len(w) > 12:
        return False

    if not w.startswith(("fl", "fly", "fle", "fli", "flick", "flik")):
        return False

    score = difflib.SequenceMatcher(None, w, TARGET).ratio()
    return score >= 0.72

def fuzzy_replace_line(line):
    def repl(match):
        word = match.group(0)
        if close_to_flyxion(word):
            return REPLACEMENT
        return word

    return re.sub(r'\b[A-Za-z]{5,12}\b', repl, line)

def normalize_text_preserving_layout(text):
    text = strip_invisible_chars(text)
    text = protect_real_words(text)

    text = KNOWN_VARIANTS.sub(REPLACEMENT, text)

    lines = text.splitlines(keepends=True)
    lines = [fuzzy_replace_line(line) for line in lines]
    text = ''.join(lines)

    text = restore_real_words(text)
    return text

with open(LOG_FILE, "a", encoding="utf-8") as log:
    log.write(f"\nFlyxion correction pass\n")
    log.write("----------------------------------------\n")

    for path in pathlib.Path(".").rglob("*"):
        if path.suffix.lower() not in extensions:
            continue
        if "backup_" in str(path):
            continue

        try:
            original = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        corrected = normalize_text_preserving_layout(original)

        if corrected != original:
            path.write_text(corrected, encoding="utf-8")
            print(f"Updated: {path}")
            log.write(f"Updated: {path}\n")
        else:
            log.write(f"[no changes] {path}\n")

    log.write("----------------------------------------\n")
    log.write("Done.\n")
PY

echo "All passes complete."