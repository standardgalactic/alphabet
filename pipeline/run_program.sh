#!/usr/bin/env bash
#
# run_program.sh — drives chapter accretion.
#
# A single pipeline.sh run writes one chapter. This wrapper is what makes
# a "program" out of that: it runs the initial seed, and whenever that run
# discovers a missing dependency (Section 5, "Dependencies", of pipeline.sh)
# it queues a new seed rather than papering over the gap. This script drains
# that queue — running each discovered dependency through the pipeline in
# turn, which may itself discover further dependencies — until the queue is
# empty or a depth cap is hit. The resulting set of chapters is a graph that
# reveals its own missing nodes as it's written, not a tree planned in full
# in advance.
#
# A processed set (by slug) prevents cycles: if two chapters end up
# depending on each other, or the same missing concept gets queued twice
# under different phrasing, this will not loop forever — it will just skip
# a slug it has already produced a chapter for.
#
# Usage:
#   ./run_program.sh SEED [MAX_DEPTH]
#
#   All the same env vars pipeline.sh accepts (MODEL, CORPUS_DIR, etc.)
#   are honored here and passed straight through to every pipeline.sh
#   invocation, including the ones spawned from the queue.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SEED="${1:?Usage: $0 SEED [MAX_DEPTH]}"
MAX_DEPTH="${2:-3}"
QUEUE_DIR="${QUEUE_DIR:-$SCRIPT_DIR/queue}"
PROCESSED_LOG="$(mktemp)"

mkdir -p "$QUEUE_DIR"

slug_full() { echo "$1" | tr '[:upper:]' '[:lower:]' | tr -cs 'a-z0-9' '-' | sed 's/^-//;s/-$//'; }

# Must mirror pipeline.sh's own FULL_SLUG computation exactly, since it's
# used both to find the queue files pipeline.sh wrote for this seed and as
# the cycle-guard key. Using a truncated slug here caused a real bug: once a
# dependency chain's combined name exceeded 40 chars, the child's computed
# slug collapsed onto the parent's, corrupting the queue and double-moving
# files. See pipeline.sh's slug_full() comment for the full explanation.
full_slug_of() {
  local p="$1"
  if [ -f "$p" ] || [ -d "$p" ]; then
    slug_full "$(basename "$p")"
  else
    slug_full "$p"
  fi
}

run_one() {
  local seed_path="$1" depth="$2"
  local key
  key="$(full_slug_of "$seed_path")"

  if grep -qxF "$key" "$PROCESSED_LOG" 2>/dev/null; then
    echo ">> [depth $depth] skipping '$key' — already processed this run (cycle guard)"
    return
  fi
  echo "$key" >> "$PROCESSED_LOG"

  echo
  echo "================================================================"
  echo ">> [depth $depth/$MAX_DEPTH] chapter: $key"
  echo "================================================================"

  if [ "$depth" -gt "$MAX_DEPTH" ]; then
    echo ">> depth cap reached — leaving '$seed_path' queued, not processing"
    echo ">>   (raise MAX_DEPTH or process it manually with pipeline.sh)"
    return
  fi

  "$SCRIPT_DIR/pipeline.sh" "$seed_path" || {
    echo ">> pipeline.sh exited non-zero for '$key' — leaving its"
    echo ">>   dependencies (if any were queued before the failure) for"
    echo ">>   manual review rather than continuing to accrete on top of"
    echo ">>   a chapter that didn't finish."
    return
  }

  # anything the run just queued gets processed next, one level deeper
  local q
  for q in "$QUEUE_DIR"/${key}--*.seed; do
    [ -e "$q" ] || continue
    run_one "$q" "$((depth + 1))"
    [ -e "$q" ] && mv "$q" "$q.done"
  done
}

run_one "$SEED" 1

echo
echo "================================================================"
echo "Program run complete. Chapters processed this run:"
sed 's/^/  - /' "$PROCESSED_LOG"
remaining="$(find "$QUEUE_DIR" -maxdepth 1 -name '*.seed' 2>/dev/null | wc -l)"
[ "$remaining" -gt 0 ] && echo "$remaining seed(s) still queued in $QUEUE_DIR/ (depth cap or not yet run)"
rm -f "$PROCESSED_LOG"
