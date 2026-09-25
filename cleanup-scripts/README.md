# Alphabet cleanup scripts

These are three alternative migrations for `standardgalactic/alphabet`. Run exactly one from the repository root. Every script defaults to a dry run, makes no commit, and leaves the worktree reviewable with `git diff` and `git status`.

`01-document-and-map.sh` changes only documentation. It preserves the existing README as `docs/README-legacy.md` and installs a concise current README plus contents, status, and related-repository maps.

`02-categorize-root.sh` installs the same updated documentation and then classifies root-level tracked files into folders. Before moving anything it scans both the repository itself and neighboring checkouts for references into `standardgalactic/alphabet`; referenced paths remain in place. Use `--scan-root=/path/to/repos` if your repositories do not share a parent directory.

`03-aggressive-reduction.sh` installs the same updated documentation, identifies captured webpages, build byproducts, obvious duplicate-download names, and root PDFs with same-basename editable sources. It protects internally and externally referenced files, then uses `git rm` to stage the remaining candidates for deletion. It makes no commit, so every deletion remains recoverable during review.

Run these commands from the root of the `alphabet` repository:

```bash
bash cleanup-scripts/01-document-and-map.sh
bash cleanup-scripts/01-document-and-map.sh --apply

bash cleanup-scripts/02-categorize-root.sh
bash cleanup-scripts/02-categorize-root.sh --apply

bash cleanup-scripts/03-aggressive-reduction.sh
bash cleanup-scripts/03-aggressive-reduction.sh --apply
```

By default, the structural scripts scan the parent directory of `alphabet` for neighboring repository checkouts that link into this repository. If the related repositories are stored somewhere else, override that location explicitly:

```bash
bash cleanup-scripts/02-categorize-root.sh --scan-root="/actual/path/to/checkouts"
```

The documentation-only script is the safest default. For either structural script, inspect the generated TSV manifest before applying and verify the GitHub Pages build afterward. External links that are not present in the scanned local repositories cannot be discovered automatically. To recover a staged deletion before committing, run `git restore --staged --worktree -- PATH`.
