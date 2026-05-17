#!/usr/bin/env python3

import re
import difflib
import pathlib
import sys

REPLACEMENT = "Flyxion"
TARGET = "flyxion"
LOG_FILE = "flyxion_corrections.log"

extensions = {".json", ".srt", ".tsv", ".txt", ".vtt"}

# --- SAFE INTERACTIVE INPUT (works even with heredoc) ---
def get_mode():
    try:
        if sys.stdin.isatty():
            mode = input(
                "Treat 'affliction/infliction' as (n)ame → replace with Flyxion, "
                "or (c)oncept → leave untouched? [n/c]: "
            ).strip().lower()
        else:
            with open("/dev/tty") as tty:
                mode = tty.readline().strip().lower()
    except Exception:
        mode = "c"

    return "n" if mode == "n" else "c"

mode = get_mode()
REPLACE_PROTECTED = (mode == "n")

# --- VARIANT REGEX ---
KNOWN_VARIANTS = re.compile(
    r'(?i)(?<![A-Za-z])('
    r'Flexion|Flixian|Flixing|Fliction|Flippshen|Flexumian|Fletchian|Flitchin|'
    r'Flyzion|Flyxen|Flyxian|Flyxionn|Flyxionne|Flykshun|Flykshion|Flikshun|'
    r'Flikzion|Flikxion|Flixion|Fleksion|Fleksian|Flextion|Flicksion|'
    r'Flickzion|Flickxion|Flickshank|Fleksheen|Flekshun|Flekzion|Flixyon|'
    r'Flixxon|Flixionne|Felician|Flyxionu|Flick Sheenan|Flicksheen|'
    r'Flickshian|Flitschian|Flickian|Flixson|Flijnen|Flitian|Flickshan|'
    r'Flickstahn|Flexiton|Flakiron|Flickshahn|Flixie|Flixan|Fugchin|'
    r'Flickshen|Flickshin|Flixgen|Flixen|Flicksham|Flitchinan|Flickening|'
    r'Fluxian|Fluxion|Flitchian|Fleishness|Flixidan|Flickshon|Flickshin|'
    r'Fleckession|Flickession|Fliccine|Felictian|Fleckstown|Lickshin|'
    r'Fluxium|Fleixing|Flixten|Flishan|Flinchin|Flickshin|Felixian|'
    r'Flick Sheehan|Folicurian|Flixium|Flickditschian|Flitschernard|'
    r'Flixim|Flixen|Fletchion|Fletuchin|Flickenden|Flixman|Flexian|'
    r'Flickshan|Flickson|Flixbyan|Flickshanth|Flection|Flixia|'
    r'Floodioxin|Flixam|Flixuen|Flickstein|Flagellian|Flexivision|'
    r'Flickishin|Flitscheon'
    r')(?![A-Za-z])'
)

# --- PROTECTION / FORCE LOGIC ---
PROTECTED = {
    "affliction": "__PROTECTED_AFFLICTION__",
    "Affliction": "__PROTECTED_CAP_AFFLICTION__",
    "infliction": "__PROTECTED_INFLICTION__",
    "Infliction": "__PROTECTED_CAP_INFLICTION__",
} if not REPLACE_PROTECTED else {}

FORCE_REPLACE = {"affliction", "infliction"} if REPLACE_PROTECTED else set()

# --- CLEANUP ---
def strip_invisible_chars(text):
    return re.sub(r'[\u200B-\u200D\uFEFF]', '', text)

def protect_real_words(text):
    for word, marker in PROTECTED.items():
        text = re.sub(rf'(?<![A-Za-z]){re.escape(word)}(?![A-Za-z])', marker, text)
    return text

def restore_real_words(text):
    for word, marker in PROTECTED.items():
        text = text.replace(marker, word)
    return text

# --- MATCH LOGIC ---
def close_to_flyxion(word):
    w = word.lower()

    if w == TARGET:
        return False

    if w in FORCE_REPLACE:
        return True

    if len(w) < 5 or len(w) > 12:
        return False

    # relaxed gate so "infliction" is reachable
    if "fl" not in w[:4]:
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

# --- MAIN NORMALIZATION ---
def normalize_text_preserving_layout(text):
    text = strip_invisible_chars(text)
    text = protect_real_words(text)

    text = KNOWN_VARIANTS.sub(REPLACEMENT, text)

    lines = text.splitlines(keepends=True)
    lines = [fuzzy_replace_line(line) for line in lines]
    text = ''.join(lines)

    text = restore_real_words(text)
    return text

# --- FILE PASS ---
with open(LOG_FILE, "a", encoding="utf-8") as log:
    log.write("\nFlyxion correction pass\n")
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

