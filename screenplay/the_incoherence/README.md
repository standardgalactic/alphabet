# The Incoherence
## A Novel in Fragments
**Author:** Flyxion  
**Engine:** LuaLaTeX (required — do not compile with pdfLaTeX or XeLaTeX)  
**Compile:** `lualatex main.tex` (run twice for cross-references)

---

## Directory Structure

```
incoherence/
├── main.tex              Master file: fonts, pagination, chapter includes
├── README.md             This file
├── fonts/                Place ALL font files here (see list below)
└── chapters/             One .tex file per chapter
    ├── 01-de-pulsu-et-causa.tex              [DRAFTED]
    ├── 02-de-lege-et-negligentia.tex         [DRAFTED]
    ├── 03-de-voce-et-flumine.tex             [DRAFTED]
    ├── 04-de-scriptura-et-fragmento.tex      [DRAFTED]
    ├── 05-de-multiplicatione-narrationum.tex [DRAFTED]
    ├── 06-de-defectu-et-calibratione.tex     [DRAFTED]
    ├── 07-de-observatione-et-dispositione.tex [DRAFTED]
    ├── 08-de-necessitate-retroactiva.tex     [DRAFTED]
    ├── 09-de-compositione-regiminum.tex      [DRAFTED]
    ├── 10-de-iteratione-et-deriva.tex        [DRAFTED]
    ├── 11-de-cognitione-non-universali.tex   [DRAFTED]
    ├── 12-de-scripturis-et-formis.tex        [DRAFTED — byobu drift begins]
    ├── 13-de-interruptione-et-aula.tex       [STUB]
    ├── 14-de-confrontatione.tex              [STUB]
    ├── 15-de-expositione-miraculi.tex        [STUB — byobu return begins]
    ├── 16-de-silentio-et-exilio.tex          [STUB — drip transformation]
    ├── 17-de-porta-et-transitu.tex           [STUB — byobu return ends]
    ├── 18-de-itinere-et-resolutione.tex      [DRAFTED — resynchronized]
    ├── 19-de-fez-et-continuatione.tex        [STUB]
    ├── 20-de-portu-et-translatione.tex       [STUB]
    ├── 21-de-scriptorium-et-copia.tex        [STUB]
    ├── 22-de-parisiis-et-dissolutione.tex    [STUB]
    └── 23-de-fine-quod-non-est-finis.tex     [STUB — write last]
```

---

## Required Fonts
Place all of the following in `./fonts/`:

```
NovaMonoStandardGalactic.ttf      — substrate, baseline reality
Sga-Regular.ttf                   — binding assertions, necessity
CursiveGalactic-Regular.ttf       — flow, dissolution
Amiri-Regular.ttf                 — Arabic, non-subordinate layer
Amiri-Bold.ttf
Amiri-Italic.ttf
Amiri-BoldItalic.ttf
Cheiro-Regular.ttf                — isolated italic, handwriting refusing to join
Clypto-Regular.ttf                — partial legibility, threshold font
Logico_philosophicus-Regular.ttf  — logical-symbolic substitution
Systada-Regular.ttf               — terminal monospace, machine substrate
Lingojam_cipher-Regular.ttf       — Unicode SGA variant (use sparingly)
dactyl.ttf                        — digit-growth font (byobu pagination drift)
shapeform.ttf                     — near-illegible (maximum stress only)
```

---

## Required Packages
Install via `tlmgr` or your distribution's package manager:

```
fontspec        unicode-math    polyglossia
geometry        fancyhdr        microtype
setspace        ragged2e        calc
multicol        paracol         marginnote
changepage      afterpage       atbegshi
tikz            rotating        graphicx
titlesec
```

On Ubuntu/WSL:
```bash
sudo apt-get install texlive-full
# or more selectively:
sudo apt-get install texlive-luatex texlive-lang-arabic texlive-fonts-extra
```

---

## Pagination System

The book runs two simultaneous page counters:

- **Left margin:** Western numerals (English side, outer edge)
- **Right margin:** Eastern Arabic-script numerals (Arabic side, inner edge)

Reading direction is from outside in on both sides.

### Byobu Drift Cycle (chapters XII–XVII)

One drift-and-return cycle occurs across six chapters:

| Chapters | Mechanism | Effect |
|----------|-----------|--------|
| XII–XIV  | Right pages split: `\rightpagesplit` steps Arabic counter **twice** per physical page | Arabic runs ahead of English |
| XV–XVII  | Left pages hold: `\leftpagecatch` holds Arabic counter while English advances | English catches up |
| XVIII+   | Both counters resynchronized | Normal pagination resumes |

During drift, Arabic numerals render in **Dactyl** font (digits grow from seed).  
During return, Western numerals render in **Dactyl**.  
No announcement is made in the text. Only numbering.

---

## Typographic Phase Map

| Phase | Chapters | State |
|-------|----------|-------|
| Stable | I–II | Nova Mono dominant. Single SGA anomaly. |
| Bifurcating | III–IV | Cursive SGA enters. Arabic as non-translated layer. Spatial fragmentation begins. |
| Propagating | V–VII | SGA escapes into connective tissue. Repetition-with-variation. Drip desynchronizes. |
| Retroactive | VIII | Typography reassigns necessity to the past without changing glyphs. |
| Midpoint | IX | Non-commuting columns. Reading order changes meaning. No privileged path. |
| Fractured | X–XI | Clypto enters unannounced. Character identity non-unified. Cognitive ontology destabilized. |
| Drift | XII–XIV | Scholastic excursus. Byobu pagination. Peak instability. Fire exposure. |
| Return | XV–XVII | Sparse equilibrium. Drip undergoes single irreversible transformation. |
| Transmission | XVIII–XXII | Fonts degraded as if copied. Approximate replication. Dispersal. |
| Normalized incoherence | XXIII | Anomalies permanent. System appears stable only because incoherence is baseline. |

---

## Key Macros (defined in main.tex)

```latex
\sga{text}      — Standard Galactic (binding assertions)
\cga{text}      — Cursive Galactic (flow, dissolution)
\logico{text}   — Logico Philosophicus (formal notation)
\cheiro{text}   — Cheiro (isolated italic forms)
\clypto{text}   — Clypto (partial legibility)
\sys{text}      — Systada (terminal/machine register)

\begin{AR}...\end{AR}   — Arabic text block (Amiri, right-to-left)

\drifttext{x}{y}{text}  — Place text at offset from page center (TikZ)
\rotblock{text}         — Rotate 180 degrees
\tiltblock{angle}{text} — Rotate by arbitrary angle

\rightpagesplit   — Step Arabic counter twice (byobu drift recto pages)
\leftpagecatch    — Hold Arabic counter (byobu return verso pages)
```

---

## Notes on Stubs

Each stub file contains:
- Full typographic state annotation
- Notes on which screenplay scenes it covers
- Notes on which structural operations should occur
- A placeholder line visible in compiled output

Stub chapters compile cleanly — the placeholder text will appear in the PDF.
Draft them in order from the outside in: XIII, XXII, XIX, XX, XXI, XIV, XV,
XVI, XVII — saving XXIII (the final page) for last.

---

## The Drip

The clepsydra motif appears in every chapter. Its state tracks the system:

| State | Chapters |
|-------|----------|
| Present, unemphasized | I |
| No longer ignorable | II |
| Distributed, not localized | III |
| Falls on parchment; text changes | IV |
| Not from the fountain | V |
| Almost simultaneous, not aligned | VI |
| Not evenly spaced | VII–VIII |
| Split across columns; irreconcilable | IX |
| Five drops, fifth out of phase | X |
| No longer audible; still present | XI |
| **Single irreversible transformation** | **XVI** |
| — | Final state TBD |
