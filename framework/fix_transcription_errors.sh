############################################
# Main normalization pass (Python, reliable)
############################################

python3 <<'PY'
import re, difflib, pathlib, sys

REPLACEMENT = "Flyxion"

PATTERN = re.compile(
    r'(?i)(?<![A-Za-z])('
    r'Flexion|Flixian|Flixing|Fliction|Flippshen|Flexumian|Fletchian|Flicksheen|'
    r'Flyzion|Flyxen|Flyxian|Flyxionn|Flyxionne|Flykshun|Flykshion|Flikshun|Flikzion|'
    r'Flikxion|Flixion|Fleksion|Fleksian|Flextion|Flicksion|Flickzion|Flickxion|'
    r'Flickshank|Fleksheen|Flekshun|Flekzion|Flixyon|Flixxon|Flixionne|Felician|'
    r'Flyxionu|Flick Sheenan|Flixan|Fugchin|Flickshen|Flickshin'
    r')(?![A-Za-z])'
)

LOG_FILE = "flyxion_corrections.log"

extensions = {".json",".srt",".tsv",".txt",".vtt"}

with open(LOG_FILE, "a", encoding="utf-8") as log:
    log.write("\nFlyxion normalization log - Python pass\n")
    log.write("----------------------------------------\n")

    for path in pathlib.Path(".").rglob("*"):
        if path.suffix.lower() not in extensions:
            continue
        if "backup_" in str(path):
            continue

        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        lines_before = text.splitlines()
        lines_after = []
        changed = False

        for line in lines_before:
            new_line = PATTERN.sub(REPLACEMENT, line)
            new_line = re.sub(r'\b(in|of|af|am|an|at|to)\s*(Flyxion)', r'\1 \2', new_line, flags=re.I)

            if new_line != line:
                changed = True

            lines_after.append(new_line)

        if changed:
            path.write_text("\n".join(lines_after), encoding="utf-8")

            log.write(f"\n---- {path} ----\n")
            diff = difflib.unified_diff(
                lines_before,
                lines_after,
                lineterm=""
            )
            for line in diff:
                log.write(line + "\n")

            print(f"Updated: {path}")
        else:
            log.write(f"[no changes] {path}\n")

    log.write("----------------------------------------\n")
    log.write("Done.\n")
PY