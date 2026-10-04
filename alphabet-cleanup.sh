#!/usr/bin/env bash
set -euo pipefail

# alphabet-cleanup.sh
#
# Conservative cleanup for the alphabet repository.
# - Recompresses selected spoken-word MP3s to 64 kbps
# - Removes disposable LaTeX build artifacts
# - Reports large files and exact duplicates
# - Reports repository size before/after
#
# Does NOT:
# - rewrite Git history
# - delete PDFs, source files, fonts, images, or music
# - remove duplicate files automatically

if [[ ! -d .git ]]; then
    echo "Error: run this from the repository root."
    exit 1
fi

command -v ffmpeg >/dev/null || {
    echo "Error: ffmpeg is required."
    exit 1
}

echo "========================================"
echo " alphabet repository cleanup"
echo "========================================"
echo

echo "Before:"
du -sh --exclude=.git .
du -sh .git
echo

# ------------------------------------------------------------
# 1. Recompress known spoken-word outliers
# ------------------------------------------------------------

spoken_audio=(
    "constraint-geometry/Why_Flat_Metrics_Fail_Reality.mp3"
    "processing/Abstraction_as_Reduction.mp3"
    "projects/Unifying_Everything_Relativistic_Scalar_Vector_Plenum.mp3"
    "cosmology/Everything_Is_Made_of_Possible_Futures.mp3"
    "projects/RSVP_Unifica_Cosmos_Mente_y_Empresas_con_Analogías.mp3"
    "projects/نظرية_كل_شيء_الكون_وعي_الشركات_بالملأ.mp3"
)

echo "Compressing selected spoken-word audio..."

for f in "${spoken_audio[@]}"; do
    if [[ ! -f "$f" ]]; then
        echo "  missing: $f"
        continue
    fi

    tmp="${f%.mp3}.cleanup-tmp.mp3"

    echo "  $f"

    if ffmpeg \
        -hide_banner \
        -loglevel error \
        -i "$f" \
        -map_metadata 0 \
        -vn \
        -c:a libmp3lame \
        -b:a 64k \
        "$tmp"
    then
        # Only replace original if compression actually helped.
        old_size=$(stat -c %s "$f")
        new_size=$(stat -c %s "$tmp")

        if (( new_size < old_size )); then
            mv "$tmp" "$f"
            saved=$((old_size - new_size))
            echo "    saved $(numfmt --to=iec-i --suffix=B "$saved")"
        else
            rm -f "$tmp"
            echo "    skipped: no size reduction"
        fi
    else
        rm -f "$tmp"
        echo "    FAILED"
    fi
done

echo

# ------------------------------------------------------------
# 2. Remove disposable LaTeX build artifacts
# ------------------------------------------------------------

echo "Removing LaTeX build artifacts..."

find . \
    -path './.git' -prune -o \
    -type f \( \
        -name '*.aux' \
        -o -name '*.bcf' \
        -o -name '*.blg' \
        -o -name '*.fdb_latexmk' \
        -o -name '*.fls' \
        -o -name '*.ilg' \
        -o -name '*.ind' \
        -o -name '*.idx' \
        -o -name '*.log' \
        -o -name '*.nav' \
        -o -name '*.out' \
        -o -name '*.snm' \
        -o -name '*.toc' \
        -o -name '*.run.xml' \
    \) \
    -print -delete

echo

# ------------------------------------------------------------
# 3. Clean temporary files left by interrupted runs
# ------------------------------------------------------------

echo "Removing cleanup temporary files..."

find . \
    -path './.git' -prune -o \
    -type f -name '*.cleanup-tmp.mp3' \
    -print -delete

echo

# ------------------------------------------------------------
# 4. Report exact duplicate files >1 MiB
# ------------------------------------------------------------

echo "Exact duplicate files larger than 1 MiB:"

find . \
    -path './.git' -prune -o \
    -type f -size +1M -print0 |
xargs -0 -r sha256sum |
sort |
awk '
{
    hash=$1
    $1=""
    sub(/^  /,"")

    if (hash == previous_hash) {
        if (!shown) {
            print ""
            print "DUPLICATE GROUP:"
            print previous_file
        }

        print
        shown=1
    } else {
        shown=0
    }

    previous_hash=hash
    previous_file=$0
}'

echo

# ------------------------------------------------------------
# 5. Report largest remaining files
# ------------------------------------------------------------

echo "Largest remaining files:"
echo

find . \
    -path './.git' -prune -o \
    -type f -printf '%s\t%p\n' |
sort -nr |
head -30 |
numfmt --field=1 --to=iec-i --suffix=B

echo

# ------------------------------------------------------------
# 6. Repository state
# ------------------------------------------------------------

echo "After:"
du -sh --exclude=.git .
du -sh .git
echo

echo "Git object database:"
git count-objects -vH

echo
echo "Changed files:"
git status --short

echo
echo "Cleanup complete."
echo "Review git status before committing."
