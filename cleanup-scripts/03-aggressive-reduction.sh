#!/usr/bin/env bash
set -Eeuo pipefail

# Aggressive but recoverable reduction. Candidates are removed with git rm,
# but no commit is made; Git can restore every removal during review.

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
stamp=$(date -u +%Y%m%dT%H%M%SZ)
manifest="cleanup-aggressive-$stamp.tsv"
declare -A protected=()
declare -a candidates=()

is_internally_referenced() {
  local needle=$1 source
  while IFS= read -r source; do
    source=${source#./}
    [[ "$source" == "$needle" || "$source" == "$manifest" ]] && continue
    return 0
  done < <(rg -IlF --glob '!.git/**' -- "$needle" . 2>/dev/null || true)
  return 1
}

if [[ -d "$scan_root" ]]; then
  while IFS= read -r linked_path; do
    [[ -n "$linked_path" ]] && protected["$linked_path"]=1
  done < <(rg -I -o 'https://github\.com/standardgalactic/alphabet/(blob|raw|tree)/[^/]+/[^ )>"#?]+' "$scan_root" 2>/dev/null \
    | sed -E 's#^.*alphabet/(blob|raw|tree)/[^/]+/##' \
    | sort -u || true)
fi

# High-confidence clutter classes only: captured pages, editor backups,
# transient build products, numbered duplicate downloads, and root renderings
# that have a same-basename editable source. All remain recoverable.
while IFS= read -r -d '' path; do
  base=$(basename "$path")
  case "$path" in
    .git/*|README.md|docs/README-legacy.md) continue ;;
  esac
  if [[ "$path" == *.mhtml || "$path" == *~ || "$path" == *.bak || "$path" == *.aux || "$path" == *.log || "$path" == *.out || "$path" == *.toc || "$path" == *.synctex.gz ]]; then
    candidates+=("$path")
  elif [[ "$base" =~ \([0-9]+\)\.[^.]+$ || "$base" =~ [_-](copy|Copy)(\.[^.]+)$ ]]; then
    candidates+=("$path")
  elif [[ "$path" != */* && "$path" == *.pdf && ( -f "${path%.pdf}.tex" || -f "${path%.pdf}.md" ) ]]; then
    candidates+=("$path")
  fi
done < <(git ls-files -z)

printf 'path\tdecision\treason\n' > "$manifest"
for path in "${candidates[@]}"; do
  if [[ -n ${protected[$path]+yes} ]]; then
    printf '%s\tkeep\tinbound link from nearby repository\n' "$path" >> "$manifest"
    continue
  fi
  if is_internally_referenced "$path"; then
    printf '%s\tkeep\tinternal reference\n' "$path" >> "$manifest"
    continue
  fi
  printf '%s\tdelete\taggressive cleanup candidate\n' "$path" >> "$manifest"
  if (( apply )); then
    git rm -- "$path"
  fi
done

echo "Wrote $manifest"
if (( apply )); then
  echo "Candidates were staged for deletion. Review git diff. Before committing, recover any path with: git restore --staged --worktree -- PATH"
else
  echo "Dry run only. Review $manifest, then re-run with --apply."
fi
