#!/usr/bin/env bash
set -Eeuo pipefail

# Categorize root-level tracked files, while protecting paths referenced by
# nearby repositories. Dry-run is the default; pass --apply to perform git mv.

apply=0
scan_root=
for arg in "$@"; do
  case "$arg" in
    --apply) apply=1 ;;
    --scan-root=*) scan_root=${arg#*=} ;;
    *) echo "Unknown argument: $arg" >&2; exit 2 ;;
  esac
done

git rev-parse --is-inside-work-tree >/dev/null 2>&1 || { echo "Run inside a Git worktree." >&2; exit 2; }
root=$(git rev-parse --show-toplevel)
cd "$root"
scan_root=${scan_root:-$(dirname "$root")}
script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
if (( apply )); then
  bash "$script_dir/01-document-and-map.sh" --apply
else
  bash "$script_dir/01-document-and-map.sh"
fi
report=.cleanup-link-impact.tsv
declare -A protected=()

is_internally_referenced() {
  local needle=$1 source
  while IFS= read -r source; do
    source=${source#./}
    [[ "$source" == "$needle" || "$source" == "$report" ]] && continue
    return 0
  done < <(rg -IlF --glob '!.git/**' -- "$needle" . 2>/dev/null || true)
  return 1
}

# Extract repository-relative targets from GitHub URLs in neighboring checkouts.
if [[ -d "$scan_root" ]]; then
  while IFS= read -r linked_path; do
    [[ -n "$linked_path" ]] && protected["$linked_path"]=1
  done < <(rg -I -o 'https://github\.com/standardgalactic/alphabet/(blob|raw|tree)/[^/]+/[^ )>"#?]+' "$scan_root" 2>/dev/null \
    | sed -E 's#^.*alphabet/(blob|raw|tree)/[^/]+/##' \
    | sort -u || true)
fi

printf 'path\tdestination\tdecision\n' > "$report"

destination_for() {
  case "${1,,}" in
    *.tex|*.bib|*.sty|*.cls) echo research/sources ;;
    *.pdf) echo research/rendered ;;
    *.md|*.txt|*.rst) echo documents ;;
    *.png|*.jpg|*.jpeg|*.gif|*.svg|*.webp) echo assets/images ;;
    *.mp3|*.wav|*.ogg|*.flac|*.m4a) echo assets/audio ;;
    *.mp4|*.webm|*.mov|*.mkv) echo assets/video ;;
    *.mhtml|*.html|*.htm) echo sources/captures ;;
    *.csv|*.tsv|*.json|*.jsonl|*.xml|*.yaml|*.yml) echo data ;;
    *.sh|*.py|*.pl|*.rb|*.js|*.ts|*.ahk|*.ps1) echo tools ;;
    *.ttf|*.otf|*.woff|*.woff2) echo archive/fonts ;;
    *) echo miscellaneous ;;
  esac
}

while IFS= read -r -d '' path; do
  case "$path" in
    */*|README.md|LICENSE|LICENSE.*|COPYING|COPYING.*|CODE_OF_CONDUCT.md|CONTRIBUTING.md|CONTENTS.md|PROJECT_STATUS.md|RELATED_REPOSITORIES.md|.gitignore|.gitattributes) continue ;;
  esac
  dest=$(destination_for "$path")/$path
  if [[ -n ${protected[$path]+yes} ]]; then
    printf '%s\t%s\tprotected: inbound link\n' "$path" "$dest" >> "$report"
    continue
  fi
  if is_internally_referenced "$path"; then
    printf '%s\t%s\tprotected: internal reference\n' "$path" "$dest" >> "$report"
    continue
  fi
  printf '%s\t%s\tmove\n' "$path" "$dest" >> "$report"
  if (( apply )); then
    mkdir -p "$(dirname "$dest")"
    git mv -- "$path" "$dest"
  fi
done < <(git ls-files -z)

echo "Wrote $report"
if (( apply )); then
  echo "Moves staged in the worktree. Inspect git diff and the impact report; no commit was made."
else
  echo "Dry run only. Review $report, then re-run with --apply."
fi
