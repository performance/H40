# Hanuman Chalisa: Structural Study Guide

This repository contains the complete source code for a rigorous, linguistically annotated study guide for the **Hanuman Chalisa**, alongside an interactive, highly dynamic SvelteKit web application.

## 📖 The Physical Book (PDF)

The heart of the project is a meticulously typeset, open-source LaTeX book (`main.pdf`) designed to provide unprecedented structural insight into the Awadhi poetry.

*   **Color-Coded Rhythm Maps:** Every syllable is tracked and mapped (Laghu/Guru) to teach the exact metrical timing of the Chaupais.
*   **Trilingual Integration:** Original Awadhi (Devanagari), Romanized IAST Transliteration, and Telugu script encodings for universal access.
*   **Deep Story Context:** Inline "Anchor Boxes" bridge the poetic stanzas with the foundational *Valmiki Ramayana* citations.

### Compiling the PDF locally

You can dynamically render the high-resolution PDF yourself!

**System Requirements:**
1.  **Compiler:** You need a modern TeX distribution (`MacTeX` on macOS, or `TeX Live` on Windows/Linux) containing `xelatex`.
2.  **Required Fonts:** Provide your system with the following typefaces:
    *   [Noto Serif Devanagari](https://fonts.google.com/specimen/Noto+Serif+Devanagari) (For Awadhi/Sanskrit)
    *   [Noto Sans Telugu](https://fonts.google.com/specimen/Noto+Sans+Telugu) (For Telugu Scripts)
    *   [Outfit](https://fonts.google.com/specimen/Outfit) (For English typography)

**Build Command:**
Run the following from the root directory to execute the build and generate the Table of Contents successfully:
```bash
xelatex -interaction=nonstopmode main.tex && xelatex -interaction=nonstopmode main.tex
```

---

## 🌐 The Interactive Web Experience (SvelteKit)

The entire LaTeX book structures are intelligently extracted and hosted inside a gorgeous, dark/light-mode reactive web application using Svelte 5.

### Building the Web App locally

**1. Data Extraction (Python):**
The text is generated via Python parsing scripts. This guarantees the web app maintains absolute parity with the LaTeX source.
```bash
python3 build_web_data.py
python3 build_static_data.py
cp -r web_data/* web/src/lib/data/
```

**2. Launching the App (Node.JS):**
Navigate to the web directory and start the Vite development server.
```bash
cd web
npm install
npm run dev
```

The application is completely decoupled and fully pre-renders as a structural static HTML/CSS footprint for lightning-fast deployments!
