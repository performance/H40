import os
import re

def clean_text(text):
    # Remove LaTeX commands like \laghu{} if they nested
    text = re.sub(r'\\[a-z]+(\[[^\]]*\])?\{([^\}]*)\}', r'\2', text)
    text = text.replace('|', '').replace('||', '').replace('।', '').replace('॥', '').replace(',', '').replace('.', '')
    return text.strip().lower()

def get_words(content, command_name):
    matches = re.findall(r'\\' + command_name + r'\{([^\}]+)\}', content)
    all_words = []
    for m in matches:
        if len(m.split()) > 1 or '।' in m or '|' in m:
            cleaned = clean_text(m)
            all_words.extend(cleaned.split())
    return all_words

def update_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    deva_words = get_words(content, 'deva')
    iast_words = get_words(content, 'textit')
    
    if not deva_words or not iast_words:
        return

    mapping = []
    for d, i in zip(deva_words, iast_words):
        mapping.append((d, i))
    
    table_pattern = re.compile(r'(\\begin\{tabularx\}.*?\\end\{tabularx\})', re.DOTALL)
    match = table_pattern.search(content)
    if not match:
        return
    table_text = match.group(1)
    
    # Split by LaTeX row delimiter \\
    rows = table_text.split('\\\\')
    new_rows = []
    map_idx = 0
    updated_count = 0
    
    for row in rows:
        if '&' not in row or 'Awadhi' in row or 'midrule' in row or 'toprule' in row or 'bottomrule' in row:
            new_rows.append(row); continue
        
        parts = row.split('&')
        col1 = parts[0].strip()
        
        if '\\deva' in col1 and '\\telu' in col1 and '\\textit' not in col1:
            deva_match = re.search(r'\\deva\{([^\}]+)\}', col1)
            if deva_match:
                table_deva_raw = clean_text(deva_match.group(1))
                table_deva_words = table_deva_raw.split()
                
                found_iast_words = []
                temp_idx = map_idx
                while temp_idx < len(mapping):
                    match_found = True
                    for k in range(len(table_deva_words)):
                        if temp_idx + k >= len(mapping) or mapping[temp_idx + k][0] != table_deva_words[k]:
                            match_found = False
                            break
                    if match_found:
                        found_iast_words = [mapping[temp_idx + k][1] for k in range(len(table_deva_words))]
                        map_idx = temp_idx + len(table_deva_words)
                        break
                    temp_idx += 1
                
                if found_iast_words:
                    iast_text = " ".join(found_iast_words)
                    icons = ""
                    for icon in ['\\gotchaicon', '\\glossaryicon']:
                        if icon in col1:
                            icons += " " + icon
                            col1 = col1.replace(icon, "").strip()
                    
                    col1 = col1.strip()
                    if col1.endswith('/'): col1 = col1[:-1].strip()
                    parts[0] = f" {col1} / \\textit{{{iast_text}}}{icons} "
                    new_rows.append("&".join(parts))
                    updated_count += 1
                    continue
        new_rows.append(row)
    
    if updated_count > 0:
        new_table_text = "\\\\".join(new_rows)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content.replace(table_text, new_table_text))
        print(f"Updated {path} ({updated_count} rows)")

def main():
    for f in os.listdir("sections"):
        if f.endswith(".tex") and ("chaupai" in f or "doha" in f):
            update_file(os.path.join("sections", f))

if __name__ == "__main__":
    main()
