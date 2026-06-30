import os
import re
import json

LATEX_DIR = '/Users/awesome/edu/H40/sections'
OUTPUT_DIR = '/Users/awesome/edu/H40/web_data'

def strip_latex(text):
    if not text: return ""
    # strip \makebox[\linewidth][l/c/r]{...} wrappers
    text = re.sub(r'\\makebox\[\\linewidth\]\[[lcr]\]\{([^}]*)\}', r'\1', text)
    # strip \textcolor{color}{text}
    text = re.sub(r'\\textcolor\{[^}]*\}\{([^}]*)\}', r'\1', text)
    # strip basic macros like \textbf, \textit, \deva, \telu, \iast
    text = re.sub(r'\\(?:textbf|textit|deva|telu|iast|guru|laghu)\{([^}]*)\}', r'\1', text)
    # catch nested or double
    text = re.sub(r'\\(?:textbf|textit|deva|telu|iast|guru|laghu)\{([^}]*)\}', r'\1', text)
    # clean newlines or spacing commands
    text = re.sub(r'\\vspace\{[^}]*\}', '', text)
    text = re.sub(r'\\newline', '\n', text)
    text = re.sub(r'\\null\\hfill', ' ', text)
    text = re.sub(r'\\par', '\n', text)
    text = re.sub(r'\s*\\\\\s*', '\n', text)
    text = re.sub(r'\\rightarrow', '→', text)
    text = re.sub(r'\$', '', text)
    # clean \gotchaicon, etc
    text = re.sub(r'\\[a-zA-Z]+icon\b', '', text)
    # cleanup extra whitespace but preserve newlines
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n\s+', '\n', text)
    return text.strip()

def parse_definitions(content):
    defs = []
    # Search for the প্রতিপদার্থঃ (Meaning of each word) table
    match = re.search(r'\\textbf\{\\deva\{प्रतिपदार्थः\}.*?\\begin\{tabularx\}\{.*?\}(.*?)\\end\{tabularx\}', content, re.DOTALL)
    if not match: return defs
    
    body = match.group(1)
    # isolate midrule to bottomrule
    body_match = re.search(r'\\midrule(.*?)\\bottomrule', body, re.DOTALL)
    if not body_match: return defs
    
    rows = body_match.group(1).strip().split('\\\\')
    for row in rows:
        if not row.strip(): continue
        cols = row.split('&')
        if len(cols) >= 3:
            # Extract all three scripts from the first column by splitting by '/'
            script_parts = [strip_latex(p.strip()) for p in cols[0].split('/')]
            
            awadhi = script_parts[0] if len(script_parts) > 0 else ""
            telugu = script_parts[1] if len(script_parts) > 1 else ""
            iast = script_parts[2] if len(script_parts) > 2 else ""
            
            sanskrit = strip_latex(cols[1])
            english = strip_latex(cols[2])
            notes = strip_latex(cols[3]) if len(cols) > 3 else ""
            
            defs.append({
                "awadhi": awadhi,
                "telugu": telugu,
                "iast": iast,
                "sanskrit": sanskrit,
                "english": english,
                "notes": notes
            })
    return defs

def parse_boxes(content):
    boxes = []
    # Anchorbox
    anchor = re.search(r'\\begin\{tcolorbox\}\[anchorbox\](.*?)\\end\{tcolorbox\}', content, re.DOTALL)
    if anchor:
        raw_anchor = anchor.group(1).strip()
        bold_match = re.search(r'\\textbf\{(.*?):\}(.*?)(?:\\vspace|$)', raw_anchor, re.DOTALL)
        if bold_match:
            title = strip_latex(bold_match.group(1).strip())
            desc = strip_latex(bold_match.group(2).strip())
            cit_match = re.search(r'\\vspace\{0\.5em\}\\newline (.*?)\\newline\\null\\hfill\\textit\{(.*?)\}', raw_anchor, re.DOTALL)
            cit_desc = strip_latex(cit_match.group(1).strip()) if cit_match else ""
            cit = strip_latex(cit_match.group(2).strip()) if cit_match else ""
            boxes.append({
                "type": "anchorbox", "title": title, "description": desc, "motivating_text": cit_desc, "citation": cit
            })
    
    # Gotchabox
    gotcha = re.search(r'\\begin\{tcolorbox\}\[gotchabox(?:.*?|)\](.*?)\\end\{tcolorbox\}', content, re.DOTALL)
    if gotcha:
        raw_gotcha = gotcha.group(1)
        items = re.findall(r'\\item (.*?)(?=\\item |\\end\{itemize\}|$)', raw_gotcha, re.DOTALL)
        cleaned_items = [strip_latex(i) for i in items if i.strip()]
        if not cleaned_items:
            ptxt = re.sub(r'\\begin\{itemize\}|\\end\{itemize\}', '', raw_gotcha)
            ptxt = strip_latex(ptxt)
            if ptxt: cleaned_items = [ptxt]
        boxes.append({"type": "gotchabox", "items": cleaned_items})
        
    return boxes

def parse_rhythm_map(content):
    lines = []
    tables = re.findall(r'\\begin\{tabularx\}(.*?)\\end\{tabularx\}', content, re.DOTALL)
    for table in tables:
        current_line = []
        row_match = re.search(r'\\hline(.*?)\\hline', table, re.DOTALL)
        if not row_match: continue
        cells = row_match.group(1).split('&')
        for cell in cells:
            syllables = []
            tokens = re.findall(r'\\(guru|laghu)\{(.*?)\}', cell)
            for t_type, char in tokens:
                syllables.append({"char": char.strip(), "weight": 2 if t_type == 'guru' else 1})
            if syllables: current_line.append(syllables)
        if current_line: lines.append(current_line)
    return lines

def parse_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    filename = os.path.basename(filepath)
    fid = filename.replace('.tex', '')
    if fid.startswith('chaupai'):
        vtype, vnum = 'chaupai', int(re.search(r'\d+', fid).group())
    elif fid.startswith('doha'):
        vtype, vnum = 'doha', int(re.search(r'\d+', fid).group())
    elif fid == 'concluding_doha':
        vtype, vnum = 'doha', 3
    else: return None

    title_match = re.search(r'^[ \t]*\\(?:sub)?section\*?\{(.*)\}[ \t]*$', content, re.MULTILINE)
    vtitle = strip_latex(title_match.group(1)) if title_match else ""

    deva_match = re.search(r'\{[^{}]*\\linespread\{1\.5\}\\selectfont(.*?)\\par\}', content, re.DOTALL)
    deva_text = strip_latex(deva_match.group(1)) if deva_match else ""
    
    telu_match = re.search(
        r'\{[^{}]*\\linespread\{1\.5\}\\selectfont.*?\\par\}'
        r'.*?\{[^{}]*\\linespread\{1\.5\}\\selectfont(.*?)\\par\}',
        content, re.DOTALL)
    telu_text = strip_latex(telu_match.group(1)) if telu_match else ""
    
    iast_match = re.search(r'\{[^{}]*\\linespread\{1\.3\}\\selectfont(.*?)\\par\}', content, re.DOTALL)
    iast_text = strip_latex(iast_match.group(1)) if iast_match else ""
    
    sans_eng_match = re.search(r'\\textbf\{\s*\\deva\{सरल-संस्कृतम्\}\s*:\}\\*(.*?)(?:\\vspace|\\newpage|\\textbf\{)', content, re.DOTALL)
    sans_text, eng_text = [], []
    if sans_eng_match:
        se_raw = sans_eng_match.group(1).strip()
        lines = [l.strip() for l in se_raw.split('\n') if l.strip()]
        for l in lines:
            if '\\deva{' in l: sans_text.append(strip_latex(l))
            else:
                l_cl = strip_latex(l)
                if l_cl: eng_text.append(l_cl)

    return {
        "id": fid, "title": vtitle, "type": vtype, "number": vnum,
        "text": {"awadhi": deva_text, "telugu": telu_text, "iast": iast_text},
        "translation": {"sanskrit": sans_text, "english": eng_text},
        "word_meanings": parse_definitions(content),
        "rhythm_map": parse_rhythm_map(content),
        "boxes": parse_boxes(content)
    }

def build_all():
    os.makedirs(os.path.join(OUTPUT_DIR, 'verses'), exist_ok=True)
    verses = []
    for filename in os.listdir(LATEX_DIR):
        if not filename.endswith('.tex') or filename.startswith('group') or filename in ['preface.tex', 'glossary.tex', 'macros.tex']:
            continue
        filepath = os.path.join(LATEX_DIR, filename)
        try:
            data = parse_file(filepath)
            if data:
                verses.append(data)
                out_path = os.path.join(OUTPUT_DIR, 'verses', f"{data['id']}.json")
                with open(out_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e: print(f"Error parsing {filename}: {e}")
            
    verses.sort(key=lambda v: (0 if v['id'] == 'doha1' else 0.5 if v['id'] == 'doha2' else 42 if v['id'] == 'concluding_doha' else v['number'] if v['type'] == 'chaupai' else 99))
    index_data = [{"id": v["id"], "title": v.get("title", ""), "type": v["type"], "number": v["number"]} for v in verses]
    with open(os.path.join(OUTPUT_DIR, 'index.json'), 'w', encoding='utf-8') as f:
        json.dump(index_data, f, ensure_ascii=False, indent=2)
    print(f"Successfully extracted {len(verses)} verses to {OUTPUT_DIR}")

if __name__ == '__main__':
    build_all()
