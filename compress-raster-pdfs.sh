#!/usr/bin/env bash
set -euo pipefail

# compress-raster-pdfs.sh
#
# Conservatively recompress large PDFs containing inefficient
# non-JPEG raster images.
#
# Requirements:
#   ghostscript
#   poppler-utils
#   qpdf
#
# Behavior:
#   - only considers PDFs larger than 10 MiB
#   - skips PDFs whose raster images are already all JPEG
#   - uses Ghostscript /printer quality
#   - validates output with qpdf
#   - only replaces the original if size falls by >= 20%
#   - preserves the original filename
#   - does not touch Git history

command -v gs        >/dev/null || { echo "Missing: ghostscript (gs)"; exit 1; }
command -v pdfimages >/dev/null || { echo "Missing: pdfimages"; exit 1; }
command -v qpdf      >/dev/null || { echo "Missing: qpdf"; exit 1; }

echo "=== Raster PDF compression ==="
echo

before=$(du -sb --exclude=.git . | cut -f1)

processed=0
skipped=0
saved=0

while IFS= read -r -d '' pdf; do

    read -r images nonjpeg < <(
        pdfimages -list "$pdf" 2>/dev/null |
        awk '
            NR > 2 && $1 ~ /^[0-9]+$/ {
                images++
                if ($9 != "jpeg")
                    nonjpeg++
            }
            END {
                printf "%d %d\n", images+0, nonjpeg+0
            }
        '
    )

    # No inefficient raster images.
    if (( images == 0 || nonjpeg == 0 )); then
        printf 'SKIP  %s (%d images, already JPEG/none)\n' \
            "$pdf" "$images"
        ((++skipped))
        continue
    fi

    old_size=$(stat -c %s "$pdf")
    tmp="${pdf%.pdf}.cleanup-tmp.pdf"

    printf '\nPDF   %s\n' "$pdf"
    printf '      %.1f MiB, %d images, %d non-JPEG\n' \
        "$(awk "BEGIN {print $old_size/1048576}")" \
        "$images" \
        "$nonjpeg"

    rm -f "$tmp"

    if ! gs \
        -sDEVICE=pdfwrite \
        -dCompatibilityLevel=1.6 \
        -dNOPAUSE \
        -dQUIET \
        -dBATCH \
        -dPDFSETTINGS=/printer \
        -sOutputFile="$tmp" \
        "$pdf"
    then
        echo "      ERROR: Ghostscript failed"
        rm -f "$tmp"
        continue
    fi

    if ! qpdf --check "$tmp" >/dev/null 2>&1; then
        echo "      ERROR: qpdf validation failed"
        rm -f "$tmp"
        continue
    fi

    new_size=$(stat -c %s "$tmp")

    # Require at least 20% savings.
    if (( new_size * 100 >= old_size * 80 )); then
        printf '      SKIP: %.1f -> %.1f MiB (insufficient saving)\n' \
            "$(awk "BEGIN {print $old_size/1048576}")" \
            "$(awk "BEGIN {print $new_size/1048576}")"

        rm -f "$tmp"
        ((++skipped))
        continue
    fi

    difference=$((old_size - new_size))

    printf '      KEEP: %.1f -> %.1f MiB; saved %.1f MiB\n' \
        "$(awk "BEGIN {print $old_size/1048576}")" \
        "$(awk "BEGIN {print $new_size/1048576}")" \
        "$(awk "BEGIN {print $difference/1048576}")"

    # Preserve original modification timestamp.
    touch -r "$pdf" "$tmp"

    mv "$tmp" "$pdf"

    saved=$((saved + difference))
    ((++processed))

done < <(
    find . \
        -path './.git' -prune -o \
        -type f \
        -name '*.pdf' \
        -size +10M \
        -print0
)

after=$(du -sb --exclude=.git . | cut -f1)

echo
echo "========================================"
echo "PDF compression complete"
echo "========================================"
printf 'Compressed: %d PDFs\n' "$processed"
printf 'Skipped:    %d PDFs\n' "$skipped"
printf 'Saved:      %.1f MiB\n' \
    "$(awk "BEGIN {print $saved/1048576}")"
printf 'Tree:       %.1f -> %.1f MiB\n' \
    "$(awk "BEGIN {print $before/1048576}")" \
    "$(awk "BEGIN {print $after/1048576}")"

echo
echo "Modified PDFs:"
git status --short -- '*.pdf' || true
