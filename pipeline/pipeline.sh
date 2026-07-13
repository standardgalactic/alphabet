#!/usr/bin/env bash
#
# pipeline.sh — chapter-writing engine for the CPR/RSVP/Repair Theory corpus
#
# This version is built around a specific claim about how these essays
# actually get written, not around generic drafting:
#
#   - Essays begin from a DISTINCTION worth preserving, not a thesis.
#     The thesis is allowed to emerge partway through the draft.
#   - Writing is exploratory: definitions and propositions accumulate
#     before a claim crystallizes, not after.
#   - Memory is externalized into structure (a persistent ledger file),
#     not held across runs in the author's head or in this process.
#   - A chapter that uses an undefined concept doesn't get patched over —
#     the missing concept gets queued as its own chapter (accretion).
#   - Abstract structure comes first; examples are witnesses of it,
#     found or built in a dedicated pass, not motivations invented early.
#   - Every essay is asked, explicitly, what survives the transformation
#     it's about (the invariant question), not just what it claims.
#
# Stages:
#   1. Distinguish  -> distinction.txt   (the seed distinction + invariant
#                                          question, extracted from raw notes)
#   2. Outline       -> outline.tex       (skeleton built from the distinction,
#                                          thesis explicitly marked TBD)
#   3. Draft         -> draft_0.tex       (exploratory chapter body, ending in
#                                          a Crystallized Claim section)
#   4. Ignite        -> admissibility gate on DISTINCTION, not thesis
#   5. Dependencies  -> queue/*.seed      (undefined concepts spawned as new
#                                          seeds for later chapters)
#   6. Rise          -> corpus_context.txt (resonance-ranked + pinned + ledger)
#   7. Persist       -> critique/revise loop, now checks for a named invariant
#   8. Witness       -> witnesses.txt     (examples instantiating each formal
#                                          object, found in a separate pass)
#   9. Audit + ledger update + finalize
#
# This does NOT decide what belongs in the chapter, what counts as a theorem,
# whether a distinction is worth pursuing, or whether this chapter is a ROOT
# or a CONTINUATION of existing work — that declaration is read from the seed
# file, never inferred, per the same boundary this system has always kept.
#
# Usage:
#   ./pipeline.sh SEED [options]
#
#   SEED is a path to a notebook file/dir of raw notes, or a short string.
#   Its first line may optionally be a continuation declaration:
#     ROOT
#     CONTINUES: repair operator, admissible continuation
#   If omitted, the run proceeds but is logged as UNSPECIFIED — the pipeline
#   will not guess this for you.
#
# Options (env vars):
#   MODEL=granite3-dense
#   ITERATIONS=3
#   OUTDIR=./runs/<slug>_<timestamp>
#   CORPUS_DIR=                 # existing .tex essays to cross-reference
#   FRAMEWORKS_FILE=config/frameworks.conf
#   PREAMBLE_FILE=config/preamble.tex
#   LEDGER_FILE=config/ledger.tsv        # cross-run externalized memory
#   CRITIQUE_LOG=config/critique_log.tsv # cross-run recurring-issue log
#   QUEUE_DIR=queue/                     # discovered-dependency seeds land here
#   CHAPTER_TITLE=               # defaults to the distinction, truncated
#   COMPILE=1                    # set 0 to skip lualatex compile attempt
#   WITNESS=1                    # set 0 to skip the witness-finding pass
#
# --- Phoenix-derived loop control (mechanics only, no cosmology) ---
#   IGNITE_RETRIES=1
#   DISSOLVE_PATIENCE=2
#   RESONANCE_TOP_K=8
#   AUDIT=1

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

SEED="${1:?Usage: $0 SEED [notebook file or topic string]}"
MODEL="${MODEL:-granite3-dense}"
ITERATIONS="${ITERATIONS:-3}"
CORPUS_DIR="${CORPUS_DIR:-}"
FRAMEWORKS_FILE="${FRAMEWORKS_FILE:-$SCRIPT_DIR/config/frameworks.conf}"
PREAMBLE_FILE="${PREAMBLE_FILE:-$SCRIPT_DIR/config/preamble.tex}"
LEDGER_FILE="${LEDGER_FILE:-$SCRIPT_DIR/config/ledger.tsv}"
CRITIQUE_LOG="${CRITIQUE_LOG:-$SCRIPT_DIR/config/critique_log.tsv}"
QUEUE_DIR="${QUEUE_DIR:-$SCRIPT_DIR/queue}"
COMPILE="${COMPILE:-1}"
WITNESS="${WITNESS:-1}"
IGNITE_RETRIES="${IGNITE_RETRIES:-1}"
DISSOLVE_PATIENCE="${DISSOLVE_PATIENCE:-2}"
RESONANCE_TOP_K="${RESONANCE_TOP_K:-8}"
AUDIT="${AUDIT:-1}"

mkdir -p "$QUEUE_DIR"
[ -f "$LEDGER_FILE" ] || printf 'slug\ttitle\tdistinction\tcontinuation\toutcome\ttimestamp\n' > "$LEDGER_FILE"
[ -f "$CRITIQUE_LOG" ] || printf 'slug\tround\tseverity\tcategories\ttimestamp\n' > "$CRITIQUE_LOG"

slug() { echo "$1" | tr '[:upper:]' '[:lower:]' | tr -cs 'a-z0-9' '-' | sed 's/^-//;s/-$//' | cut -c1-40; }

# slug() is truncated to 40 chars and is fine for OUTDIR names, where a
# timestamp already disambiguates. It is NOT safe for queue filenames: a
# chain of dependencies builds names by prefixing the parent's slug
# (parent--term.seed), and once that combined name exceeds 40 characters,
# truncation silently drops the newest suffix and collapses a child's
# filename onto its parent's — causing the child to overwrite the very
# seed file it was spawned from. slug_full() is the untruncated version,
# used for anything that needs to stay distinct across a dependency chain:
# the queue filename itself, and the ledger/critique-log identity column.
slug_full() { echo "$1" | tr '[:upper:]' '[:lower:]' | tr -cs 'a-z0-9' '-' | sed 's/^-//;s/-$//'; }

if [ -f "$SEED" ] || [ -d "$SEED" ]; then
  RAW_SEED_TEXT="$(cat "$SEED"/* 2>/dev/null || cat "$SEED")"
  SLUG="$(slug "$(basename "$SEED")")"
  FULL_SLUG="$(slug_full "$(basename "$SEED")")"
else
  RAW_SEED_TEXT="$SEED"
  SLUG="$(slug "$SEED")"
  FULL_SLUG="$(slug_full "$SEED")"
fi

# ---------------------------------------------------------------------------
# Continuation declaration: read, never inferred. If the first non-blank
# line is "ROOT" or "CONTINUES: ...", it's stripped from the seed text and
# recorded. Otherwise the run proceeds but is logged as UNSPECIFIED rather
# than having the pipeline guess at something that belongs to the author.
# ---------------------------------------------------------------------------

first_line="$(echo "$RAW_SEED_TEXT" | sed -n '1{/^\s*$/!p}')"
if echo "$first_line" | grep -qiE '^ROOT\s*$'; then
  CONTINUATION_DECL="ROOT"
  SEED_TEXT="$(echo "$RAW_SEED_TEXT" | sed '1d')"
elif echo "$first_line" | grep -qiE '^CONTINUES:'; then
  CONTINUATION_DECL="$first_line"
  SEED_TEXT="$(echo "$RAW_SEED_TEXT" | sed '1d')"
else
  CONTINUATION_DECL="UNSPECIFIED"
  SEED_TEXT="$RAW_SEED_TEXT"
fi

OUTDIR="${OUTDIR:-$SCRIPT_DIR/runs/${SLUG}_$(date +%Y%m%d_%H%M%S)}"
mkdir -p "$OUTDIR"
echo "$SEED_TEXT" > "$OUTDIR/seed.txt"

echo "== Model: $MODEL | Iterations: $ITERATIONS | Out: $OUTDIR"
echo "== Continuation: $CONTINUATION_DECL"
[ "$CONTINUATION_DECL" = "UNSPECIFIED" ] && \
  echo "   (no ROOT/CONTINUES declared in seed — proceeding, but this is not inferred for you)"
[ -n "$CORPUS_DIR" ] && echo "== Corpus: $CORPUS_DIR" || echo "== Corpus: (none — skipping cross-reference)"

# ---------------------------------------------------------------------------
# Vocabulary (pinned terms bypass resonance ranking — see frameworks.conf)
# ---------------------------------------------------------------------------

raw_vocab_list() { grep -vE '^\s*(#|\s*$)' "$FRAMEWORKS_FILE"; }
vocab_list()     { raw_vocab_list | sed 's/^!//'; }
pinned_terms()   { raw_vocab_list | grep '^!' | sed 's/^!//'; }

vocab_block() {
  echo "The following terms already have established meanings in the corpus."
  echo "Use them consistently; do not silently redefine or repurpose them:"
  echo
  vocab_list | sed 's/^/  - /'
}

# ---------------------------------------------------------------------------
# RISE — resonance-ranked corpus retrieval, pinning override, plus the
# externalized-memory ledger. The ledger is read here as an additional,
# always-consulted source: it is the pipeline's own accumulated record of
# what earlier runs established, independent of grep-matching raw .tex prose,
# and it is what lets a later chapter "remember" an earlier one's distinction
# even when the corpus directory itself is sparse.
# ---------------------------------------------------------------------------

corpus_scan() {
  local draft_file="$1" out_file="$2"
  : > "$out_file"

  if [ -f "$LEDGER_FILE" ] && [ "$(wc -l < "$LEDGER_FILE")" -gt 1 ]; then
    {
      echo "### Ledger — prior chapters on record (externalized memory)"
      tail -n +2 "$LEDGER_FILE" | awk -F'\t' '{print "- " $2 " — distinction: " $3 " (" $4 ", " $5 ")"}'
      echo
    } >> "$out_file"
  fi

  if [ -z "$CORPUS_DIR" ] || [ ! -d "$CORPUS_DIR" ]; then
    [ -s "$out_file" ] || echo "(no corpus configured)" > "$out_file"
    return
  fi

  local term count scored_file selected_file
  scored_file="$(mktemp)"; selected_file="$(mktemp)"

  while IFS= read -r term; do
    grep -qiF "$term" "$draft_file" 2>/dev/null || continue
    count="$(grep -riFc "$term" "$CORPUS_DIR" --include='*.tex' 2>/dev/null | awk -F: '{s+=$2} END{print s+0}')" || count=0
    [ "$count" -gt 0 ] && printf '%d\t%s\n' "$count" "$term" >> "$scored_file"
  done < <(vocab_list)

  sort -rn "$scored_file" | head -n "$RESONANCE_TOP_K" > "$selected_file"

  while IFS= read -r term; do
    grep -qiF "$term" "$draft_file" 2>/dev/null || continue
    already="$(awk -F'\t' -v t="$term" '$2==t{print "yes"; exit}' "$selected_file")"
    [ "$already" = "yes" ] && continue
    count="$(awk -F'\t' -v t="$term" '$2==t{print $1}' "$scored_file")"
    [ -n "$count" ] && printf '%d\t%s\t(pinned)\n' "$count" "$term" >> "$selected_file"
  done < <(pinned_terms)

  while IFS=$'\t' read -r count term note; do
    hits="$(grep -riF -A2 -B2 "$term" "$CORPUS_DIR" --include='*.tex' 2>/dev/null | head -n 10)" || true
    [ -z "$hits" ] && continue
    {
      if [ -n "$note" ]; then
        echo "### $term  (resonance: $count hits — included via pin, not rank)"
      else
        echo "### $term  (resonance: $count hits elsewhere in corpus)"
      fi
      echo "$hits"; echo
    } >> "$out_file"
  done < "$selected_file"
  rm -f "$scored_file" "$selected_file"

  [ -s "$out_file" ] || echo "(no resonant terms found)" > "$out_file"
  tail -c 6000 "$out_file" > "$out_file.tmp" && mv "$out_file.tmp" "$out_file"
}

# ---------------------------------------------------------------------------
# Prompt builders
# ---------------------------------------------------------------------------

write_distinguish_prompt() {
  local f="$1"
  {
    echo "You are not summarizing these notes and not producing an outline."
    echo "Your only job is to name the single distinction they are circling:"
    echo "a contrast between two things (A vs B) that the eventual essay will"
    echo "treat as worth preserving or worth taking seriously. The notes may"
    echo "be messy, incomplete, or list several ideas — find the one"
    echo "distinction underneath them that everything else depends on."
    echo
    echo "Also name the invariant question this distinction raises: what"
    echo "survives some transformation, reconstruction, projection, or"
    echo "correction, in a way that makes the distinction matter."
    echo
    echo "Output exactly two lines, nothing else:"
    echo "DISTINCTION: <side A> vs <side B>"
    echo "INVARIANT_QUESTION: What survives <the relevant operation>?"
    echo
    echo "--- RAW NOTES ---"
    echo "$SEED_TEXT"
  } > "$f"
}

write_outline_prompt() {
  local f="$1" distinction_file="$2"
  {
    echo "You are outlining a chapter for a large interconnected theoretical"
    echo "program (constraint/projection/reachability, admissibility, repair"
    echo "theory, continuation geometry, distinguishability geometry, RSVP)."
    echo "The chapter begins from the distinction below, not from a thesis."
    echo "Produce a LaTeX section skeleton only: \\section, \\subsection"
    echo "headers and one-line descriptions of what each section will"
    echo "explore if the distinction is taken seriously. Do NOT state a"
    echo "conclusion or thesis in the outline — mark the final section as"
    echo "'Crystallized Claim (TBD — to emerge during drafting)'. Include a"
    echo "line noting which established primitives this chapter depends on"
    echo "and whether it introduces new ones."
    echo
    echo "--- SEED DISTINCTION ---"
    cat "$distinction_file"
    echo
    vocab_block
    echo
    echo "--- RAW NOTES ---"
    echo "$SEED_TEXT"
  } > "$f"
}

write_draft_prompt() {
  local f="$1" outline_file="$2"
  {
    echo "Write a full chapter draft in LaTeX (amsart theorem environments:"
    echo "theorem, proposition, lemma, corollary, definition, remark, example"
    echo "are already defined — just use them). Follow the outline, but write"
    echo "it as an exploration, not a report: accumulate definitions and"
    echo "propositions that follow from taking the seed distinction"
    echo "seriously, and let the main claim emerge from that accumulation"
    echo "rather than stating it in the opening paragraph. Do not open with"
    echo "'This chapter argues that...' or any equivalent pre-announcement."
    echo "Rigorous but not padded: every claim either argued or marked as a"
    echo "conjecture. Definitions before use. End with a final subsection"
    echo "titled 'Crystallized Claim' that states, in one paragraph, whatever"
    echo "claim the preceding exploration actually arrived at — this is"
    echo "written last and is allowed to be narrower or different from"
    echo "whatever the outline anticipated. No \\documentclass or preamble —"
    echo "body content only, starting from \\section{...}."
    echo
    vocab_block
    echo
    echo "--- OUTLINE ---"
    cat "$outline_file"
  } > "$f"
}

write_ignite_prompt() {
  local f="$1" draft_file="$2"
  {
    echo "You are a minimal admissibility gate, not an editor. This draft is"
    echo "exploratory by design and is NOT required to have a thesis stated"
    echo "up front — the thesis is allowed to emerge only in the final"
    echo "'Crystallized Claim' section. Check ONLY:"
    echo
    echo "  1. Is there an identifiable DISTINCTION being explored — some"
    echo "     contrast or pair the draft is actually working with — visible"
    echo "     somewhere in the first section, even if no conclusion is"
    echo "     drawn from it yet?"
    echo "  2. Is every technical term used before it's introduced actually"
    echo "     defined somewhere in the draft (even informally)?"
    echo "  3. Does the draft have more than one section with actual content"
    echo "     (not just headers), AND does it end with a 'Crystallized"
    echo "     Claim' section stating what emerged?"
    echo
    echo "Answer with exactly one line: 'ADMITTED' if all three hold,"
    echo "'REJECTED: <reason>' if any fail. One sentence of reason max."
    echo
    echo "--- DRAFT ---"
    cat "$draft_file"
  } > "$f"
}

write_dependency_prompt() {
  local f="$1" draft_file="$2"
  {
    echo "Read this draft as an editor checking for unbuilt foundations, not"
    echo "for prose quality. List every technical term or concept the draft"
    echo "USES in a load-bearing way but does NOT itself define, AND that is"
    echo "not in the established vocabulary list below. Each such concept is"
    echo "a missing dependency: something that would need its own chapter"
    echo "before this one is fully grounded, even if this draft is otherwise"
    echo "fine as exploratory writing."
    echo
    echo "For each one, output one line:"
    echo "DEPENDENCY: <short name> — <one sentence on what a chapter"
    echo "defining it would need to establish>"
    echo
    echo "If there are none, output exactly: DEPENDENCIES: NONE"
    echo
    vocab_block
    echo
    echo "--- DRAFT ---"
    cat "$draft_file"
  } > "$f"
}

write_critique_prompt() {
  local f="$1" draft_file="$2" corpus_file="$3"
  {
    echo "You are a rigorous, adversarial editor reviewing a chapter draft"
    echo "from an interconnected formal research program. Do NOT rewrite it."
    echo "Only critique. Quote exact passages. Cover:"
    echo
    echo "1. Unsupported or overstated claims"
    echo "2. Structural problems: weak transitions, redundant sections"
    echo "3. Hand-wavy reasoning presented as if it were rigorous"
    echo "4. Missing definitions for terms used before they're defined"
    echo "5. Terminology drift against the vocabulary + corpus excerpts below"
    echo "6. Theorem/proposition statements that don't earn their status"
    echo "7. Invariance: does the draft explicitly name what survives the"
    echo "   transformation, reconstruction, or operation it concerns — or"
    echo "   does it only assert claims without ever asking what is"
    echo "   preserved? Flag if no invariant is named anywhere."
    echo
    echo "End with exactly three lines:"
    echo "SEVERITY: <integer 0-10, where 0 = no substantive issues, 10 = fundamentally broken>"
    echo "VERDICT: <'MAJOR REVISION NEEDED', 'MINOR POLISH ONLY', or 'NO SUBSTANTIVE ISSUES REMAIN'>"
    echo "CATEGORIES: <comma-separated list of which of checks 1-7 were flagged, or NONE>"
    echo
    vocab_block
    echo
    echo "--- CORPUS CROSS-REFERENCE (how these terms are used elsewhere) ---"
    cat "$corpus_file"
    echo
    echo "--- DRAFT ---"
    cat "$draft_file"
  } > "$f"
}

write_revise_prompt() {
  local f="$1" draft_file="$2" critique_file="$3"
  {
    echo "Revise the chapter draft below to resolve every issue in the"
    echo "critique. Preserve the exploratory structure and the fact that the"
    echo "thesis lives in the 'Crystallized Claim' section, not the opening."
    echo "Preserve LaTeX theorem environments. Do not add meta-commentary."
    echo "Output ONLY the revised LaTeX body (no \\documentclass, no preamble)."
    echo
    echo "--- DRAFT ---"
    cat "$draft_file"
    echo
    echo "--- CRITIQUE ---"
    cat "$critique_file"
  } > "$f"
}

write_witness_prompt() {
  local f="$1" draft_file="$2"
  {
    echo "The abstract structure of this chapter (its definitions and"
    echo "propositions) comes first; your job is to find or construct"
    echo "WITNESSES for it — concrete examples that instantiate each formal"
    echo "object, not motivating examples that came before it. For every"
    echo "\\definition, \\proposition, \\theorem, or \\lemma in the draft,"
    echo "either point to a passage in the draft that already witnesses it"
    echo "concretely, or construct one new concrete example that does."
    echo
    echo "Output one entry per formal object:"
    echo "WITNESS: <short name of the object> — <the concrete example, one"
    echo "to three sentences>"
    echo
    echo "If the draft has no formal objects to witness, output exactly:"
    echo "NO FORMAL OBJECTS TO WITNESS"
    echo
    echo "--- DRAFT ---"
    cat "$draft_file"
  } > "$f"
}

write_audit_prompt() {
  local f="$1" seed_text_file="$2" distinction_file="$3" final_file="$4"
  {
    echo "This chapter began from a DISTINCTION, not a fixed thesis — the"
    echo "thesis was allowed to emerge during drafting, in the 'Crystallized"
    echo "Claim' section. Compare the ORIGINAL SEED DISTINCTION against what"
    echo "the FINAL DRAFT actually crystallized. A different thesis than"
    echo "anyone could have predicted in advance is expected and fine; what"
    echo "matters is whether the final claim is still a serious exploration"
    echo "of the SAME distinction, or whether it quietly substituted a"
    echo "different distinction, dropped the original contrast, or hedged it"
    echo "into vagueness."
    echo
    echo "Answer with one line: 'FAITHFUL' or 'DRIFTED: <what changed>'."
    echo
    echo "--- ORIGINAL SEED NOTES ---"
    cat "$seed_text_file"
    echo
    echo "--- SEED DISTINCTION ---"
    cat "$distinction_file"
    echo
    echo "--- FINAL DRAFT ---"
    cat "$final_file"
  } > "$f"
}

run_ollama() { ollama run "$MODEL" < "$1"; }

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

echo "[1/9] Distinguish — extracting the seed distinction..."
write_distinguish_prompt "$OUTDIR/prompt_distinguish.txt"
run_ollama "$OUTDIR/prompt_distinguish.txt" > "$OUTDIR/distinction.txt"
cat "$OUTDIR/distinction.txt" | sed 's/^/      /'
DISTINCTION_LINE="$(grep -i '^DISTINCTION:' "$OUTDIR/distinction.txt" | head -1)"
CHAPTER_TITLE="${CHAPTER_TITLE:-${DISTINCTION_LINE#*: }}"
[ -z "$CHAPTER_TITLE" ] && CHAPTER_TITLE="$SEED_TEXT"

echo "[2/9] Outlining..."
write_outline_prompt "$OUTDIR/prompt_outline.txt" "$OUTDIR/distinction.txt"
run_ollama "$OUTDIR/prompt_outline.txt" > "$OUTDIR/outline.tex"

echo "[3/9] Drafting chapter body (exploratory)..."
write_draft_prompt "$OUTDIR/prompt_draft.txt" "$OUTDIR/outline.tex"
run_ollama "$OUTDIR/prompt_draft.txt" > "$OUTDIR/draft_0.tex"

echo "[4/9] Ignite — admissibility gate (distinction, not thesis)..."
attempt=0
while :; do
  write_ignite_prompt "$OUTDIR/prompt_ignite.txt" "$OUTDIR/draft_0.tex"
  run_ollama "$OUTDIR/prompt_ignite.txt" > "$OUTDIR/ignite_$attempt.txt"
  if grep -qi "^ADMITTED" "$OUTDIR/ignite_$attempt.txt"; then
    echo "      ADMITTED"; break
  fi
  echo "      REJECTED: $(grep -i "^REJECTED" "$OUTDIR/ignite_$attempt.txt" | head -1)"
  attempt=$((attempt + 1))
  if [ "$attempt" -gt "$IGNITE_RETRIES" ]; then
    echo "      gate failed after $IGNITE_RETRIES retries — aborting."
    exit 2
  fi
  echo "      redrafting (attempt $attempt)..."
  run_ollama "$OUTDIR/prompt_draft.txt" > "$OUTDIR/draft_0.tex"
done

echo "[5/9] Dependency scan — checking for unbuilt foundations..."
write_dependency_prompt "$OUTDIR/prompt_dependency.txt" "$OUTDIR/draft_0.tex"
run_ollama "$OUTDIR/prompt_dependency.txt" > "$OUTDIR/dependencies.txt"
dep_count=0
while IFS= read -r line; do
  term="$(echo "$line" | sed -E 's/^DEPENDENCY:\s*//; s/\s*—.*$//')"
  guess="$(echo "$line" | sed -E 's/^[^—]*—\s*//')"
  [ -z "$term" ] && continue
  dep_count=$((dep_count + 1))
  qfile="$QUEUE_DIR/${FULL_SLUG}--$(slug_full "$term").seed"
  {
    echo "CONTINUES: $CHAPTER_TITLE"
    echo "$term — $guess"
  } > "$qfile"
  echo "      queued dependency: $term  -> $qfile"
done < <(grep -i '^DEPENDENCY:' "$OUTDIR/dependencies.txt" || true)
[ "$dep_count" -eq 0 ] && echo "      no missing dependencies found"

echo "[6/9] Rise — resonance-ranked corpus scan (+ ledger)..."
corpus_scan "$OUTDIR/draft_0.tex" "$OUTDIR/corpus_context.txt"

echo "[7/9] Persist — critique/revise loop..."
draft_file="$OUTDIR/draft_0.tex"
prev_severity=999
stall_count=0
loop_outcome="EXHAUSTED"
for i in $(seq 1 "$ITERATIONS"); do
  echo "      iter $i: critiquing..."
  write_critique_prompt "$OUTDIR/prompt_critique_$i.txt" "$draft_file" "$OUTDIR/corpus_context.txt"
  run_ollama "$OUTDIR/prompt_critique_$i.txt" > "$OUTDIR/critique_$i.txt"

  severity="$(grep -oiE 'SEVERITY:[[:space:]]*[0-9]+' "$OUTDIR/critique_$i.txt" | grep -oE '[0-9]+' | head -1)"
  [ -z "$severity" ] && severity=5
  categories="$(grep -oiE 'CATEGORIES:.*' "$OUTDIR/critique_$i.txt" | head -1 | sed -E 's/^CATEGORIES:\s*//')"
  printf '%s\t%s\t%s\t%s\t%s\n' "$FULL_SLUG" "$i" "$severity" "${categories:-NONE}" "$(date -Iseconds)" >> "$CRITIQUE_LOG"
  echo "      severity: $severity/10  categories: ${categories:-NONE}"

  if grep -qi "NO SUBSTANTIVE ISSUES REMAIN" "$OUTDIR/critique_$i.txt" || [ "$severity" -eq 0 ]; then
    echo "      converged — no substantive issues remain"
    loop_outcome="CONVERGED"; break
  fi

  if [ "$severity" -ge "$prev_severity" ]; then stall_count=$((stall_count + 1)); else stall_count=0; fi
  prev_severity="$severity"

  if [ "$stall_count" -ge "$DISSOLVE_PATIENCE" ]; then
    echo "      DISSOLVED — severity has not improved for $DISSOLVE_PATIENCE rounds"
    loop_outcome="DISSOLVED"; break
  fi

  echo "      revising..."
  write_revise_prompt "$OUTDIR/prompt_revise_$i.txt" "$draft_file" "$OUTDIR/critique_$i.txt"
  run_ollama "$OUTDIR/prompt_revise_$i.txt" > "$OUTDIR/draft_$i.tex"
  draft_file="$OUTDIR/draft_$i.tex"
  corpus_scan "$draft_file" "$OUTDIR/corpus_context.txt"
done
[ "$loop_outcome" = "EXHAUSTED" ] && echo "      EXHAUSTED — hit iteration budget without converging or dissolving"
echo "$loop_outcome" > "$OUTDIR/loop_outcome.txt"

if [ "$WITNESS" = "1" ]; then
  echo "[8/9] Witness — finding concrete instances of the abstract structure..."
  write_witness_prompt "$OUTDIR/prompt_witness.txt" "$draft_file"
  run_ollama "$OUTDIR/prompt_witness.txt" > "$OUTDIR/witnesses.txt"
  wc_count=$(grep -ci '^WITNESS:' "$OUTDIR/witnesses.txt" || true)
  echo "      $wc_count formal object(s) witnessed — see $OUTDIR/witnesses.txt"
else
  echo "[8/9] Witness — skipped (WITNESS=0)"
fi

audit_note=""
if [ "$AUDIT" = "1" ]; then
  echo "[9/9] Audit — checking final draft against seed distinction..."
  write_audit_prompt "$OUTDIR/prompt_audit.txt" "$OUTDIR/seed.txt" "$OUTDIR/distinction.txt" "$draft_file"
  run_ollama "$OUTDIR/prompt_audit.txt" > "$OUTDIR/audit.txt"
  if grep -qi "^FAITHFUL" "$OUTDIR/audit.txt"; then
    echo "      FAITHFUL — final draft still explores the seed distinction"
  else
    echo "      DRIFTED — see $OUTDIR/audit.txt for what changed"
    audit_note="  ⚠ Audit flagged drift from original distinction: $OUTDIR/audit.txt"
  fi
else
  echo "[9/9] Audit — skipped (AUDIT=0)"
fi

echo "Updating ledger (externalized memory)..."
DISTINCTION_TEXT="$(grep -i '^DISTINCTION:' "$OUTDIR/distinction.txt" | head -1 | sed -E 's/^DISTINCTION:\s*//')"
printf '%s\t%s\t%s\t%s\t%s\t%s\n' \
  "$FULL_SLUG" "$CHAPTER_TITLE" "$DISTINCTION_TEXT" "$CONTINUATION_DECL" "$loop_outcome" "$(date -Iseconds)" \
  >> "$LEDGER_FILE"

echo "Finalizing..."
BIBFILE="${SLUG}"
sed -e "s/__TITLE__/$CHAPTER_TITLE/" \
    -e "s/__ABSTRACT__/Draft chapter generated via the distinction-first pipeline. Abstract pending author review./" \
    -e "s/__BIBFILE__/$BIBFILE/" \
    "$PREAMBLE_FILE" | sed -e "/__BODY__/{
      r $draft_file
      d
    }" > "$OUTDIR/final_chapter.tex"

touch "$OUTDIR/${BIBFILE}.bib"
cp "$draft_file" "$OUTDIR/final_body.tex"

if [ "$COMPILE" = "1" ] && command -v lualatex >/dev/null 2>&1; then
  echo "      compiling with lualatex..."
  ( cd "$OUTDIR" && lualatex -interaction=nonstopmode final_chapter.tex >/dev/null 2>&1 ) \
    && echo "      compiled: $OUTDIR/final_chapter.pdf" \
    || echo "      lualatex reported errors — see $OUTDIR/final_chapter.log"
elif [ "$COMPILE" = "1" ]; then
  echo "      lualatex not found — skipping compile (final_chapter.tex still written)"
fi

echo
echo "Done."
echo "  Distinction:      $OUTDIR/distinction.txt"
echo "  Outline:           $OUTDIR/outline.tex"
echo "  Final body:         $OUTDIR/final_body.tex"
echo "  Full document:      $OUTDIR/final_chapter.tex"
echo "  Witnesses:          $OUTDIR/witnesses.txt"
echo "  Corpus context:     $OUTDIR/corpus_context.txt"
echo "  Ledger (all runs):   $LEDGER_FILE"
[ "$dep_count" -gt 0 ] && echo "  Queued dependencies: $dep_count new seed(s) in $QUEUE_DIR/"
[ -n "$audit_note" ] && echo "$audit_note"
echo "  All intermediates in $OUTDIR/"
