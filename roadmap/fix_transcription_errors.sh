#!/usr/bin/env bash
set -euo pipefail

REPLACEMENT="Flyxion"
LOG_FILE="corrections.log"
CANDIDATE_FILE="$(mktemp)"
VIM_SCRIPT="$(mktemp)"
MATCH_FILE="$(mktemp)"

PATTERN='FLECTION|FLICTION|Felican|Felician|Felictian|Felixian|Flaccion|Flagellian|Flakirin|Flakiron|Flaxian|Flixnian|Flaxion|Flaxon|Flaxson|Fleckession|Fleckstown|Flection|Flectional|Fleekshin|Fleishness|Fleishon|Flixenian|Fluxinian|Fleixing|Fleksheen|Flekshun|Fleksian|Fleksion|Flekzion|Fletchen|Fletcher|Fletchian|Fletchion|Fletian|Fletuchin|Flexian|Flexion|Flexition|Flexiton|Flexivision|Flextion|Flexumian|Fliccine|Flickditschian|Flickenden|Flickening|Flickession|Flickian|Flickiewen|Flickishin|Flicklian|Flickpnam|Flickrinnian|Flickshahn|Flicksham|Flickshan|Flickshane|Flickshank|Flickshanth|Flicksheen|Flicksheens|Flickshen|Flickshenman|Flickshian|Flickshin|Flickshion|Flickshon|Flicksion|Flickson|Flickshorn|Flickstahn|Flickstein|Flickxion|Flickzion|Fliction|Flictionon|Flijnen|Flikshun|Flikstian|Flikxion|Flikzion|Flinchin|Flipchin|Flipchian|Flippshen|Flipschen|Flischin|Flisham|Flishan|Flishen|Flitchian|Flitchin|Flitchinan|Flitian|Flitschen|Flixton|Flixieman|Flicksheim|Flickshinen|Flieckshien|Flixioon|Flickshim|Flitscheon|Flitschernard|Flitschian|Flixam|Flixan|Flixbyan|Flixchan|Flixchen|Flixen|Flixgen|Flixheen|Flixia|Flixian|Flickin|Flixidan|Flixie|Flixien|Flixim|Flixing|Flixingen|Flixion|Flixionne|Flixium|Flixjan|Flixman|Flixon|Flixson|Flixten|Flixtion|Flixuen|Flixxion|Flixxon|Flixyon|Floodioxin|Fluxian|Fluxin|Fluxion|Fluxium|Fluxunian|Flykem|Flykshion|Flykshun|Flyxen|Flyxian|Flyxionn|Flyxionne|Flyxionu|Flyzion|Folicurian|Fouiches|Fuchin|Fugchin|Liction|Slikin|Flick Sheenan|Flick Sheehan|Flick Sheenum|Flick Sheen'

cleanup() {
  rm -f "$CANDIDATE_FILE" "$VIM_SCRIPT" "$MATCH_FILE"
}
trap cleanup EXIT

############################################
# Counters / timing
############################################

FILES_SCANNED=0
FILES_UPDATED=0
FILES_UNCHANGED=0
SECONDS=0

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
  echo "================================================================"
  echo "Flyxion correction run — $(date '+%Y-%m-%d %H:%M:%S')"
  echo "Backup snapshot: $BACKUP_DIR"
  echo "================================================================"
} >> "$LOG_FILE"

############################################
# Interactive affliction/infliction disambiguation
############################################

echo "---- Interactive disambiguation: affliction / infliction (txt only) ----"

while IFS= read -r -d '' file; do
  python3 - "$file" "$LOG_FILE" <<'PY'
import sys
import re

filename = sys.argv[1]
log_file = sys.argv[2]
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
log_entries = []
quit_requested = False

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
            quit_requested = True
            break

        if resp == "n":
            original = line.strip()
            lines[i] = pattern.sub("Flyxion", line)
            modified = True
            log_entries.append(f"  L{i+1}: {original}")
            log_entries.append(f"        -> {lines[i].strip()}")
        else:
            log_entries.append(f"  L{i+1}: kept as-is [{resp}]: {line.strip()}")

# Save any progress made before a quit, rather than discarding it.
if modified:
    with open(filename, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print(f"Updated (affliction/infliction pass): {filename}")

if log_entries:
    with open(log_file, "a", encoding="utf-8") as lf:
        lf.write(f"\n[affliction/infliction] {filename}\n")
        lf.write("\n".join(log_entries) + "\n")

if quit_requested:
    print("Disambiguation stopped early for this file (quit).")
PY
done < <(find . -type f -name "*.txt" ! -path "./backup_*/*" -print0)

############################################
# Vim script
############################################

cat > "$VIM_SCRIPT" <<EOF
let g:flyxion_matches = []
g/\\v\\c(^|[^A-Za-z])(${PATTERN})([^A-Za-z]|$)/call add(g:flyxion_matches, line('.') . "\\x01" . getline('.'))
call writefile(g:flyxion_matches, '${MATCH_FILE}')
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

      FILES_SCANNED=$((FILES_SCANNED + 1))

      before_hash="$(sha256sum "$file" | awk '{print $1}')"

      : > "$MATCH_FILE"
      vim -Es "$file" -S "$VIM_SCRIPT" >/dev/null 2>&1 || true

      after_hash="$(sha256sum "$file" | awk '{print $1}')"

      if [ "$before_hash" != "$after_hash" ]; then
        FILES_UPDATED=$((FILES_UPDATED + 1))
        match_count=0

        {
          echo ""
          echo "[substitution] $file"
        } >> "$LOG_FILE"

        if [ -s "$MATCH_FILE" ]; then
          while IFS=$'\x01' read -r lineno before_text; do
            [ -z "$lineno" ] && continue
            printf '  L%s: %s\n' "$lineno" "$before_text" >> "$LOG_FILE"
            match_count=$((match_count + 1))
          done < "$MATCH_FILE"
        fi

        echo "  ($match_count line(s) changed)" >> "$LOG_FILE"
        echo "Updated: $file"
      else
        FILES_UNCHANGED=$((FILES_UNCHANGED + 1))
      fi

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

if [ -s "$CANDIDATE_FILE" ]; then
  CANDIDATE_COUNT="$(sort -u "$CANDIDATE_FILE" | wc -l | tr -d ' ')"
  {
    echo ""
    echo "==== Candidate Variants (aggregated, $CANDIDATE_COUNT unique) ===="
    sort "$CANDIDATE_FILE" | uniq -c | sort -nr
  } >> "$LOG_FILE"
else
  CANDIDATE_COUNT=0
  echo "" >> "$LOG_FILE"
  echo "==== Candidate Variants (none found) ====" >> "$LOG_FILE"
fi

############################################
# Summary
############################################

{
  echo ""
  echo "==== Summary ===="
  echo "Files scanned        : $FILES_SCANNED"
  echo "Files updated        : $FILES_UPDATED"
  echo "Files unchanged      : $FILES_UNCHANGED"
  echo "Unique candidates    : $CANDIDATE_COUNT"
  echo "Elapsed time         : ${SECONDS}s"
  echo ""
  echo "================================================================"
  echo "Run complete — $(date '+%Y-%m-%d %H:%M:%S')"
  echo "================================================================"
} >> "$LOG_FILE"

echo "Done. Log written to: $LOG_FILE"
echo "Backup saved to: $BACKUP_DIR"
