import os
import re
import json

LATEX_DIR = '/Users/awesome/edu/H40/sections'
OUTPUT_DIR = '/Users/awesome/edu/H40/web_data'

def strip_latex(text):
    if not text: return ""
    # strip \makebox[\linewidth][l/c/r]{...} wrappers (used for doha 4-line layout)
    text = re.sub(r'\\makebox\[\\linewidth\]\[[lcr]\]\{([^}]*)\}', r'\1', text)
    # strip basic macros like \textbf, \textit, \deva, \telu
    text = re.sub(r'\\(?:textbf|textit|deva|telu|guru|laghu)\{([^}]*)\}', r'\1', text)
    # catch nested or double
    text = re.sub(r'\\(?:textbf|textit|deva|telu|guru|laghu)\{([^}]*)\}', r'\1', text)
    # clean newlines or spacing commands
    text = re.sub(r'\\vspace\{[^}]*\}', ' ', text)
    text = re.sub(r'\\newline', ' ', text)
    text = re.sub(r'\\null\\hfill', ' ', text)
    text = re.sub(r'\\par', ' ', text)
    text = re.sub(r'\\\\', ' ', text)
    text = re.sub(r'\\rightarrow', '→', text)
    text = re.sub(r'\$', '', text)
    # clean \gotchaicon, etc
    text = re.sub(r'\\[a-zA-Z]+icon\b', '', text)
    # cleanup extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def parse_boxes(content):
    boxes = []
    # Anchorbox
    anchor = re.search(r'\\begin\{tcolorbox\}\[anchorbox\](.*?)\\end\{tcolorbox\}', content, re.DOTALL)
    if anchor:
        raw_anchor = anchor.group(1).strip()
        # Parse title, text, citation
        bold_match = re.search(r'\\textbf\{(.*?):\}(.*?)(?:\\vspace|$)', raw_anchor, re.DOTALL)
        if bold_match:
            title = strip_latex(bold_match.group(1).strip())
            desc = strip_latex(bold_match.group(2).strip())
            
            # The citation part usually follows \vspace{0.5em}\newline {text}\newline\null\hfill\textit{cit}
            cit_match = re.search(r'\\vspace\{0\.5em\}\\newline (.*?)\\newline\\null\\hfill\\textit\{(.*?)\}', raw_anchor, re.DOTALL)
            cit_desc = strip_latex(cit_match.group(1).strip()) if cit_match else ""
            cit = strip_latex(cit_match.group(2).strip()) if cit_match else ""
            
            boxes.append({
                "type": "anchorbox",
                "title": title,
                "description": desc,
                "motivating_text": cit_desc,
                "citation": cit
            })
    
    # Gotchabox
    gotcha = re.search(r'\\begin\{tcolorbox\}\[gotchabox(?:.*?|)\](.*?)\\end\{tcolorbox\}', content, re.DOTALL)
    if gotcha:
        raw_gotcha = gotcha.group(1)
        items = re.findall(r'\\item (.*?)(?=\\item |\\end\{itemize\}|$)', raw_gotcha, re.DOTALL)
        cleaned_items = [strip_latex(i) for i in items if i.strip()]
        
        # some gotchas don't have items, just text
        if not cleaned_items:
            # strip itemize block and just get text
            ptxt = re.sub(r'\\begin\{itemize\}|\\end\{itemize\}', '', raw_gotcha)
            ptxt = strip_latex(ptxt)
            if ptxt: cleaned_items = [ptxt]
            
        boxes.append({
            "type": "gotchabox",
            "items": cleaned_items
        })
        
    # Appreciationbox
    appr = re.search(r'\\begin\{tcolorbox\}\[appreciationbox(?:.*?|)\](.*?)\\end\{tcolorbox\}', content, re.DOTALL)
    if appr:
        boxes.append({
            "type": "appreciationbox",
            "content": strip_latex(appr.group(1))
        })
        
    return boxes

def parse_definitions(content):
    defs = []
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
            awadhi = strip_latex(cols[0].split('/')[0]) # take the deva part
            sanskrit = strip_latex(cols[1])
            english = strip_latex(cols[2])
            notes = strip_latex(cols[3]) if len(cols) > 3 else ""
            defs.append({
                "awadhi": awadhi,
                "sanskrit": sanskrit,
                "english": english,
                "notes": notes
            })
    return defs

def parse_rhythm_map(content):
    lines = []
    # Find all table environments, typically there are two for Chaupai (Line 1, Line 2)
    tables = re.findall(r'\\begin\{tabularx\}(.*?)\\end\{tabularx\}', content, re.DOTALL)
    
    for table in tables:
        current_line = []
        # The row with rhythm has \textbf{\guru... or \textbf{\laghu...
        row_match = re.search(r'\\hline(.*?)\\hline', table, re.DOTALL)
        if not row_match: continue
        
        cells = row_match.group(1).split('&')
        for cell in cells:
            syllables = []
            # extract all \guru{x} and \laghu{y}
            tokens = re.findall(r'\\(guru|laghu)\{(.*?)\}', cell)
            for t_type, char in tokens:
                syllables.append({
                    "char": char.strip(),
                    "weight": 2 if t_type == 'guru' else 1
                })
            if syllables:
                current_line.append(syllables)
        
        if current_line:
            lines.append(current_line)
            
    # filter out the definition table if it got caught (it shouldn't because it doesn't have guru/laghu)
    return lines

def parse_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Determine ID and Type
    filename = os.path.basename(filepath)
    fid = filename.replace('.tex', '')
    if fid.startswith('chaupai'):
        vtype = 'chaupai'
        vnum = int(re.search(r'\d+', fid).group())
    elif fid.startswith('doha'):
        vtype = 'doha'
        vnum = int(re.search(r'\d+', fid).group())
    elif fid == 'concluding_doha':
        vtype = 'doha'
        vnum = 3
    else:
        return None

    # Parse text blocks
    # Devanagari — first \linespread{1.5} block
    deva_match = re.search(r'\{[^{}]*\\linespread\{1\.5\}\\selectfont(.*?)\\par\}', content, re.DOTALL)
    deva_text = strip_latex(deva_match.group(1)) if deva_match else ""
    
    # Telugu — second \linespread{1.5} block
    telu_match = re.search(
        r'\{[^{}]*\\linespread\{1\.5\}\\selectfont.*?\\par\}'
        r'.*?\{[^{}]*\\linespread\{1\.5\}\\selectfont(.*?)\\par\}',
        content, re.DOTALL)
    telu_text = strip_latex(telu_match.group(1)) if telu_match else ""
    
    # IAST — first \linespread{1.3} block
    iast_match = re.search(r'\{[^{}]*\\linespread\{1\.3\}\\selectfont(.*?)\\par\}', content, re.DOTALL)
    iast_text = strip_latex(iast_match.group(1)) if iast_match else ""
    
    # Simple Sanskrit Translation
    sans_eng_match = re.search(r'\\subsubsection\*\{\\textbf\{\\deva\{सरल-संस्कृतम्\} :\}\}(.*?)(?:\\vspace|\Z)', content, re.DOTALL)
    sans_text = ""
    eng_text = ""
    if sans_eng_match:
        se_raw = sans_eng_match.group(1).strip()
        lines = [l.strip() for l in se_raw.split('\\\\') if l.strip()]
        
        # reconstruct lines
        s_lines = []
        e_lines = []
        for l in lines:
            if '\\deva{' in l:
                s_lines.append(strip_latex(l))
            else:
                l_cl = strip_latex(l)
                if l_cl: e_lines.append(l_cl)
        
        sans_text = [l for l in s_lines if l]
        eng_text = [l for l in e_lines if l]

    data = {
        "id": fid,
        "type": vtype,
        "number": vnum,
        "text": {
            "awadhi": deva_text,
            "telugu": telu_text,
            "iast": iast_text
        },
        "translation": {
            "sanskrit": sans_text,
            "english": eng_text
        },
        "word_meanings": parse_definitions(content),
        "rhythm_map": parse_rhythm_map(content),
        "boxes": parse_boxes(content)
    }

    return data

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
                
                # Write individual file
                out_path = os.path.join(OUTPUT_DIR, 'verses', f"{data['id']}.json")
                with open(out_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error parsing {filename}: {e}")
            
    # Write master index
    verses.sort(key=lambda x: (x['type'] != 'doha', x['number'])) # doha 1, doha 2, chaupais, conluding doha
    
    # Custom sort for sequence:
    def get_seq(v):
        if v['id'] == 'doha1': return 0
        if v['id'] == 'doha2': return 0.5  # immediately after doha1, before chaupais
        if v['type'] == 'chaupai': return v['number']
        if v['id'] == 'concluding_doha': return 42
        return 99
        
    verses.sort(key=get_seq)
    
    index_data = [{"id": v["id"], "type": v["type"], "number": v["number"]} for v in verses]
    with open(os.path.join(OUTPUT_DIR, 'index.json'), 'w', encoding='utf-8') as f:
        json.dump(index_data, f, ensure_ascii=False, indent=2)
        
    print(f"Successfully extracted {len(verses)} verses to {OUTPUT_DIR}")

if __name__ == '__main__':
    build_all()
