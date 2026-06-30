#!/usr/bin/env bash
set -euo pipefail
BLENDER=${BLENDER:-blender}
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GENERATOR=${1:-rsvp_hypercell}
CONFIG=${CONFIG:-"$ROOT_DIR/configs/render.default.json"}
PARAMS=${PARAMS:-}
OUTPUT_DIR=${OUTPUT_DIR:-"$ROOT_DIR/output_v4"}
LOG_DIR=${LOG_DIR:-"$ROOT_DIR/logs_v4"}
mkdir -p "$OUTPUT_DIR" "$LOG_DIR"
BLEND_OUT="$OUTPUT_DIR/${GENERATOR}.blend"
META_OUT="$OUTPUT_DIR/${GENERATOR}.metadata.json"
PNG_PREFIX="$OUTPUT_DIR/${GENERATOR}_"
LOG="$LOG_DIR/${GENERATOR}.log"
ARGS=(--generator "$GENERATOR" --config "$CONFIG" --blend-out "$BLEND_OUT" --metadata-out "$META_OUT")
if [[ -n "$PARAMS" ]]; then ARGS+=(--params "$PARAMS"); fi
PYTHONPATH="$ROOT_DIR" "$BLENDER" -b --python "$ROOT_DIR/flyxion_sim/scene_runner.py" -- "${ARGS[@]}" > "$LOG" 2>&1
"$BLENDER" -b "$BLEND_OUT" -o "$PNG_PREFIX" -f 1 >> "$LOG" 2>&1
if [[ -f "$OUTPUT_DIR/${GENERATOR}_0001.png" ]]; then mv "$OUTPUT_DIR/${GENERATOR}_0001.png" "$OUTPUT_DIR/${GENERATOR}.png"; fi
echo "[v4] Rendered $GENERATOR -> $OUTPUT_DIR/${GENERATOR}.png"
