# Licensing

This repository mixes work by its author with fonts by other people, so no
single licence can honestly cover every file. The rule is: each file is under
the licence of whoever made it, and the author's own work is dedicated to the
public domain.

## The author's own work: CC0 1.0 (public domain)

`LICENSE` is the CC0 1.0 Universal dedication. It applies to everything in
this repository that the author wrote or drew, namely:

* the Python scripts, shell scripts, tests and HTML viewers;
* the README, notes, text corpora and other documentation;
* generated experiment data and indexes (JSON, logs, images, `.g2n` projects)
  produced by those scripts from CC0 inputs;
* the hand-drawn glyphs of the author's own faces, once listed in the table
  below as `author`.

## Fonts

| File(s) | Status | Licence |
|---|---|---|
| `Amiri-*.ttf` | Third party (Khaled Hosny and the Amiri project) | SIL OFL 1.1, see `licenses/OFL-1.1.txt` |
| `NovaMonoStandardGalactic.ttf` | Modified Version of NovaMono (Wojciech Kalinowski, "wmk69", Copyright (c) 2011, Reserved Font Name "NovaMono") | SIL OFL 1.1 only. It cannot be CC0 or GPL. Under OFL clause 3 a Modified Version must not use the Reserved Font Name, so the file should be renamed (the family name inside the font as well as the filename) |
| `Systada*.ttf/.svg/.woff*` | Mixed: some glyphs hand-drawn by the author, scanned and built with Calligraphr; others taken from a free typeface | **To be completed.** Hand-drawn glyphs: author (CC0). Borrowed glyphs: licence of the source typeface, not yet identified. Until the source is named, treat the file as not cleared for redistribution under CC0 |
| `Sga-Regular.*`, `CursiveGalactic-Regular.*`, `Cheiro-Regular.*`, `Clypto-Regular.*`, `Logico_philosophicus-Regular.*`, `Lingojam_cipher-Regular.ttf`, `shapeform.*`, `dactyl.ttf` | Provenance not recorded | **To be completed.** For each, record whether it is the author's own drawing (then CC0) or someone else's (then their licence) |
| `experiments*/`, `styled_fonts/`, `alterations/`, `output/` | Fonts generated from the files above by the scripts | Same licence as the source font they were generated from. A font generated from an OFL font is OFL; from a CC0 font, CC0 |

## Why the earlier GPL-3.0 notice was replaced

GPL-3.0 is a software licence, and applying it to the whole repository
asserted terms over third-party OFL fonts that the OFL does not allow
(OFL clause 5: the Font Software must be distributed entirely under the OFL
and not under any other licence), and it conflicted with the author's
public-domain publishing practice for his own work.

## How to complete the table

For every font file marked "To be completed", one of three statements is true
and should replace the entry:

1. `author`: drawn by the author. Licence CC0.
2. `third party, <name>, <licence>`: copy the licence text into `licenses/`.
3. `mixed`: list the glyph groups under each of the above.

This file is a statement of the author's intent and of the licences the
third-party files already carry. It is not legal advice.
