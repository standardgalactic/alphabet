#!/usr/bin/env bash
set -euo pipefail

REPLACEMENT="Flyxion"
LOG_FILE="flyxion_corrections.log"
CANDIDATE_FILE="$(mktemp)"
VIM_SCRIPT="$(mktemp)"

PATTERN='FLECTION|FLICTION|Felican|Felician|Felictian|Felixian|Flaccion|Flagellian|Flakirin|Flakiron|Flaxian|Flaxion|Flaxon|Flaxson|Fleckession|Fleckstown|Flection|Flectional|Fleekshin|Fleishness|Fleishon|Fleixing|Fleksheen|Flekshun|Fleksian|Fleksion|Flekzion|Fletchen|Fletcher|Fletchian|Fletchion|Fletian|Fletuchin|Flexian|Flexion|Flexition|Flexiton|Flexivision|Flextion|Flexumian|Fliccine|Flickditschian|Flickenden|Flickening|Flickession|Flickian|Flickiewen|Flickishin|Flicklian|Flickpnam|Flickrinnian|Flickshahn|Flicksham|Flickshan|Flickshane|Flickshank|Flickshanth|Flicksheen|Flicksheens|Flickshen|Flickshian|Flickshin|Flickshion|Flickshon|Flicksion|Flickson|Flickstahn|Flickstein|Flickxion|Flickzion|Fliction|Flictionon|Flijnen|Flikshun|Flikstian|Flikxion|Flikzion|Flinchin|Flipchin|Flippshen|Flipschen|Flischin|Flisham|Flishan|Flishen|Flitchian|Flitchin|Flitchinan|Flitian|Flitschen|Flitscheon|Flitschernard|Flitschian|Flixam|Flixan|Flixbyan|Flixchan|Flixchen|Flixen|Flixgen|Flixheen|Flixia|Flixian|Flixidan|Flixie|Flixien|Flixim|Flixing|Flixingen|Flixion|Flixionne|Flixium|Flixjan|Flixman|Flixon|Flixson|Flixten|Flixtion|Flixuen|Flixxion|Flixxon|Flixyon|Floodioxin|Fluxian|Fluxin|Fluxion|Fluxium|Fluxunian|Flykem|Flykshion|Flykshun|Flyxen|Flyxian|Flyxionn|Flyxionne|Flyxionu|Flyzion|Folicurian|Fouiches|Fuchin|Fugchin|Slikin|Flick Sheenan|Flick Sheehan|Flick Sheenum|Flick Sheen'

cleanup() {
  rm -f "$CANDIDATE_FILE" "$VIM_SCRIPT"
}
trap cleanup EXIT

############################################
# Backup snapshot
############################################

TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
BACKUP_DIR="backup_$TIMESTAMP"

echo "Creating backup snapshot: $BACKUP_DIR"
mkdir -p "$BACKUP_DIR"

while IFS= read -r -d '' file; do
  mkdir -p "$BACKUP_DIR/$(dirname "$file")"
  cp "$file" "$BACKUP_DIR/$file"
done < <(find . -type f \( \
  -name "*.json" -o -name "*.srt" -o -name "*.tsv" -o -name "*.txt" -o -name "*.vtt" \
\) ! -path "./backup_*/*" -print0)

echo "Backup complete."

############################################
# Logging init
############################################

{
  echo ""
  echo "Flyxion normalization log - $(date)"
  echo "----------------------------------------"
} >> "$LOG_FILE"

############################################
# Interactive affliction/infliction disambiguation
############################################

echo "---- Interactive disambiguation: affliction / infliction (txt only) ----"

while IFS= read -r -d '' file; do
  python3 - "$file" <<'PY'
import sys
import re

filename = sys.argv[1]
pattern = re.compile(r'\b([Aa]ffliction|[Ii]nfliction)\b')

try:
    tty = open("/dev/tty")
except Exception:
    sys.exit(0)

def ask(prompt):
    print(prompt, end='', flush=True)
    return tty.readline().strip().lower()

try:
    with open(filename, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
except Exception:
    sys.exit(0)

modified = False

for i, line in enumerate(lines):
    if pattern.search(line):
        print("\n---")
        print(f"{filename}:{i+1}")
        print(line.strip())

        while True:
            resp = ask("Is this the name (n) or the concept (c)? [n/c/skip/quit]: ")
            if resp in ("n", "c", "skip", "quit"):
                break

        if resp == "quit":
            sys.exit(0)

        if resp == "n":
            lines[i] = pattern.sub("Flyxion", line)
            modified = True

if modified:
    with open(filename, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print(f"Updated (affliction/infliction pass): {filename}")
PY
done < <(find . -type f -name "*.txt" ! -path "./backup_*/*" -print0)

############################################
# Vim script
############################################

cat > "$VIM_SCRIPT" <<EOF
redir! > /dev/stdout
g/\\v\\c(^|[^A-Za-z])(${PATTERN})([^A-Za-z]|$)/echo expand('%:p') . ':' . line('.') . ': ' . getline('.')
redir END
%s/\\v\\c(^|[^A-Za-z])(${PATTERN})([^A-Za-z]|$)/\\1${REPLACEMENT}\\3/g
%s/\\v\\c(in|of|af|am|an|at|to)(flyxion)/\\1 Flyxion/g
%s/\\v\\coblocosm/oblicosm/g
wq!
EOF

############################################
# Main normalization pass
############################################

while IFS= read -r -d '' file; do
  case "$file" in
    *.json|*.srt|*.tsv|*.txt|*.vtt)

      tmp_log="$(mktemp)"

      before_hash="$(sha256sum "$file" | awk '{print $1}')"

      vim -Es "$file" -S "$VIM_SCRIPT" > "$tmp_log" 2>/dev/null || true

      after_hash="$(sha256sum "$file" | awk '{print $1}')"

      if [ "$before_hash" != "$after_hash" ]; then
        echo "Updated: $file"
        echo "Updated: $file" >> "$LOG_FILE"
        if [ -s "$tmp_log" ]; then
          cat "$tmp_log" >> "$LOG_FILE"
        fi
      else
        echo "[no changes] $file" >> "$LOG_FILE"
      fi

      rm -f "$tmp_log"

      python3 -c '
import sys, difflib, re

target = "flyxion"
threshold = 0.60
filename = sys.argv[1]

prefixes = (
    "fl", "fly", "fli", "fle", "flu",
    "flek", "flex", "flix", "flux",
    "flyk", "flet", "flic", "flit"
)

try:
    with open(filename, "r", encoding="utf-8", errors="ignore") as fh:
        for line in fh:
            for w in re.findall(r"[A-Za-z]{5,18}", line):
                lw = w.lower()

                if lw == target:
                    continue

                if not lw.startswith(prefixes):
                    continue

                score = difflib.SequenceMatcher(None, lw, target).ratio()

                if score >= threshold or any(x in lw for x in ("xion", "xian", "xen", "zion", "ksh", "shun", "shion")):
                    print(lw)
except Exception:
    pass
' "$file" >> "$CANDIDATE_FILE"

      ;;
  esac
done < <(find . -type f ! -path "./backup_*/*" -print0)

############################################
# Candidate aggregation
############################################

echo "" >> "$LOG_FILE"

if [ -s "$CANDIDATE_FILE" ]; then
  echo "---- Candidate Variants (aggregated) ----" >> "$LOG_FILE"
  sort "$CANDIDATE_FILE" | uniq -c | sort -nr >> "$LOG_FILE"
else
  echo "---- Candidate Variants (none found) ----" >> "$LOG_FILE"
fi

echo "----------------------------------------" >> "$LOG_FILE"
echo "Done." >> "$LOG_FILE"

echo "Done. Log written to: $LOG_FILE"
echo "Backup saved to: $BACKUP_DIR"
