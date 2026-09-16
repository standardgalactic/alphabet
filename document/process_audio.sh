#!/usr/bin/env bash

set -euo pipefail

echo "=== Converting M4A to MP3 ==="

shopt -s nullglob
m4as=( *.m4a )

if [ ${#m4as[@]} -gt 0 ]; then
    for file in "${m4as[@]}"; do
        ffmpeg -n -i "$file" -vn -acodec libmp3lame -ab 192k "${file%.m4a}.mp3"
    done

    echo "=== Moving original M4A files to parent directory ==="
    mv -- *.m4a ..
fi

echo "=== Slowing MP3 files ==="

for f in *.mp3; do
    ffmpeg -y -i "$f" \
        -filter_complex "asetrate=44100*0.95,atempo=1.03,aresample=44100" \
        -q:a 0 "temp_$f"

    mv "temp_$f" "$f"
done

echo "=== Running Whisper transcription ==="

whisper *.mp3

echo "=== Compressing MP3 files ==="

for f in *.mp3; do
    ffmpeg -y -i "$f" -vn -ab 64k "compressed_$f"
    mv "compressed_$f" "$f"
done

echo "=== Done ==="
