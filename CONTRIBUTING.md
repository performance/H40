# Contributing to the Hanuman Chalisa Study Guide

Thank you for your interest in contributing! This document explains the full build pipeline in the **correct order**.

---

## Repository Structure

```
/
├── main.tex                  # LaTeX master document
├── sections/                 # One .tex file per verse (40 chaupais + dohas)
├── web/                      # SvelteKit web application
│   └── src/lib/data/         # Pre-generated JSON data (committed, do not edit by hand)
├── docs/                     # Reference documentation
│   └── awadhi_grammar_sources.md
├── build_web_data.py         # Step 3a: Extract verse data from .tex → JSON
├── build_static_data.py      # Step 3b: Extract preface, glossary → JSON/MD
├── apply_hsizes.py           # Utility: re-synchronize rhythm map grid geometry
├── audit_hsizes.py           # Utility: detect mismatched hsize matrices
└── CONTRIBUTING.md           # This file
```

---

## Full Build Pipeline

Run these steps **in order** whenever you edit `.tex` source files.

### Step 1 — Edit LaTeX source

Edit files in `sections/`. Each verse has its own file (e.g. `sections/chaupai16.tex`).

### Step 2 — Compile the PDF

Run `xelatex` **twice** — the second pass is required to build the Table of Contents correctly.

```bash
xelatex -interaction=nonstopmode main.tex
xelatex -interaction=nonstopmode main.tex
```

**Required fonts** (install before first compile):
- [Noto Serif Devanagari](https://fonts.google.com/specimen/Noto+Serif+Devanagari)
- [Noto Sans Telugu](https://fonts.google.com/specimen/Noto+Sans+Telugu)

The output PDF is `main.pdf`. Copy it to the web static folder:

```bash
cp main.pdf web/static/Hanuman_Chalisa_Study_Guide.pdf
```

### Step 3 — Re-generate JSON data from LaTeX

These scripts parse the `.tex` files and output structured JSON. Run both:

```bash
python3 build_web_data.py      # → web_data/ (43 verse JSON files)
python3 build_static_data.py   # → intro.md, glossary.json
```

### Step 4 — Copy generated data into the web app

```bash
cp -r web_data/verses web/src/lib/data/
cp web_data/index.json web/src/lib/data/index.json
```

> **Note:** `web_data/` is gitignored (intermediate output). Only `web/src/lib/data/` is committed.

### Step 5 — Build the web application

```bash
cd web
npm install        # Only needed once, or after package.json changes
npm run build      # Outputs to web/build/
```

To preview locally before committing:
```bash
npm run dev        # Live dev server at http://localhost:5173
```

---

## Rhythm Map Geometry Utilities

If you add a new verse or change syllable weights, the rhythm map grid geometry may need re-synchronization. Use these tools:

```bash
python3 audit_hsizes.py    # Detect tables where hsize fractions don't match matra counts
python3 apply_hsizes.py    # Patch detected mismatches automatically
```

---

## Linguistic Conventions

- **Script:** Awadhi in Devanagari, with Telugu transliteration side-by-side
- **Matra counting:** Laghu (light) = 1, Guru (heavy) = 2. Conjuncts follow standard Sanskrit prosody with Śithila exceptions documented in poetryboxes
- **Phonetic shift notation:** Use `\deva{व} $\rightarrow$ \deva{ब}` pattern in gotchaboxes
- **Anusvara:** Use chandrabindu (ँ) for nasalized vowels in song context, regular anusvara (ं) for standard orthography

---

## Commit Style

This project uses conventional commits:

| Prefix | When to use |
|--------|-------------|
| `fix(content):` | Corrections to verse text, notes, or boxes |
| `feat(content):` | New explanatory boxes or sections |
| `fix(latex):` | LaTeX structure or compilation fixes |
| `chore(web):` | Web rebuild or data sync |
| `docs:` | README, CONTRIBUTING, or reference updates |
