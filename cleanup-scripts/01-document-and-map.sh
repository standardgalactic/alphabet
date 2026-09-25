#!/usr/bin/env bash
set -Eeuo pipefail

# Documentation-only cleanup for standardgalactic/alphabet.
# Dry-run is the default. Pass --apply to write files.

apply=0
[[ ${1:-} == "--apply" ]] && apply=1

git rev-parse --is-inside-work-tree >/dev/null 2>&1 || { echo "Run inside a Git worktree." >&2; exit 2; }
root=$(git rev-parse --show-toplevel)
cd "$root"

write_file() {
  local path=$1
  if (( apply )); then
    mkdir -p "$(dirname "$path")"
    printf '%s\n' "$2" > "$path"
    echo "wrote $path"
  else
    echo "would write $path"
  fi
}

readme='# Standard Galactic Alphabet

`alphabet` began as a collection of fonts, keyboards, translators, ciphers, and visual experiments surrounding the Standard Galactic Alphabet. It subsequently expanded into a long-running art and research project concerned with technological fashion, speculative systems, interface culture, technical rhetoric, and the ways experimental ideas become products, doctrines, or abandoned futures.

The repository now contains essays, research notes, software experiments, visual works, recordings, source material, and unfinished investigations. It is an active conceptual workspace rather than a single-purpose font package. Some components have matured into separate repositories; material retained here also documents the project’s development and may not be its current maintained version.

## Navigate

- [Contents](CONTENTS.md)
- [Project and work status](PROJECT_STATUS.md)
- [Related repositories](RELATED_REPOSITORIES.md)
- [Historical README](docs/README-legacy.md)
- [Live site](https://standardgalactic.github.io/alphabet/)

## Status vocabulary

Works may be marked **active**, **stable**, **complete**, **continuing**, **extracted**, **historical**, **fragment**, **superseded**, or **unclassified**. Repository-wide activity should not be inferred from the last modification date of this README.

## Origins and early works

The repository’s earlier visual presentation is preserved in [the historical README](docs/README-legacy.md). It covers the alphabet, keyboards, translators, ciphers, Cistercian numbers, Dactyl, and other early experiments.'

contents='# Contents

This is a navigational map, not an exhaustive inventory. It should describe conceptual relationships rather than merely group files by extension.

## Alphabet and early visual work

Document the font, translators, keyboards, ciphers, live demonstrations, and retained historical material here.

## Research and essays

Link the principal subject directories and their local indexes here. Each work should identify its canonical source and current status.

## Software and experiments

Link runnable projects, prototypes, demonstrations, and their supported environments here.

## Art, sound, and moving image

Link visual works, recordings, animations, and related source material here.

## Sources and archives

Identify captured webpages, references, transcripts, and intentionally historical collections here.

## Related repositories

See [RELATED_REPOSITORIES.md](RELATED_REPOSITORIES.md) for components continued elsewhere.'

status='# Project Status

This repository is an active conceptual workspace and a historical collection. Its components do not share one software-release lifecycle.

| Status | Meaning |
|---|---|
| Active | Currently changing or receiving new work |
| Stable | Intentionally usable in its present form |
| Complete | Finished as an essay, artwork, or experiment |
| Continuing | Conceptually open without implying frequent maintenance |
| Extracted | Continued in another repository |
| Historical | Preserved as evidence of an earlier project state |
| Fragment | Incomplete material retained intentionally |
| Superseded | Replaced by a named later version |
| Unclassified | Not yet reviewed |

## Component register

Add one row per important work or component with its status, canonical source, rendered artifact, successor, and last substantive revision.'

related='# Related Repositories

This file maps projects that originated in or remain conceptually related to `alphabet`.

| Repository | Relationship | Status here | Canonical location |
|---|---|---|---|
| `standardgalactic/fonts` | Font work spun out of this repository | Extracted | https://github.com/standardgalactic/fonts |

Add further repositories as extracted component, active successor, independent experiment, supporting tool, or archive.'

if [[ -f README.md ]]; then
  if (( apply )); then
    mkdir -p docs
    [[ -e docs/README-legacy.md ]] || cp -- README.md docs/README-legacy.md
    echo "preserved README.md as docs/README-legacy.md"
  else
    echo "would preserve README.md as docs/README-legacy.md"
  fi
fi

write_file README.md "$readme"
write_file CONTENTS.md "$contents"
write_file PROJECT_STATUS.md "$status"
write_file RELATED_REPOSITORIES.md "$related"

if (( ! apply )); then
  echo "Dry run only. Re-run with --apply after reviewing this plan."
fi

