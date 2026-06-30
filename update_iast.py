import os
import re

def clean_iast(text):
    text = re.sub(r'\\textit\{([^}]+)\}', r'\1', text)
    text = text.replace('|', ' ').replace('||', ' ').replace(',', ' ')
    return text.lower().strip()

def extract_iast_words(content):
    matches = re.findall(r'\\textit\{([^}]+)\}', content)
    words = []
    for match in matches:
        if '|' in match or '||' in match:
            cleaned = clean_iast(match)
            words.extend(cleaned.split())
    return words

def update_table(content, iast_words):
    table_regex = re.compile(r'(\\begin\{tabularx\}.*?\\end\{tabularx\})', re.DOTALL)
    match = table_regex.search(content)
    if not match:
        return content, False
    
    table_text = match.group(1)
    rows = table_text.split('\\\\')
    updated_rows = []
    idx = 0
    updated_count = 0
    
    for row in rows:
        if '&' not in row or 'Awadhi' in row or 'midrule' in row or 'toprule' in row or 'bottomrule' in row:
            updated_rows.append(row)
            continue
        
        parts = row.split('&')
        col1 = parts[0].strip()
        
        # Check if it has Devanagari AND Telugu but NO IAST yet
        if '\\deva' in col1 and '\\telu' in col1 and '\\textit' not in col1:
            deva_match = re.search(r'\\deva\{([^\}]+)\}', col1)
            num_words = 1
            if deva_match:
                # Count words in Devanagari, handle some exceptions if needed
                dev_text = deva_match.group(1).strip()
                num_words = len(dev_text.split())
            
            if idx + num_words <= len(iast_words):
                found_iast = " ".join(iast_words[idx : idx + num_words])
                
                icons = ""
                for icon in ['\\gotchaicon', '\\glossaryicon']:
                    if icon in col1:
                        icons += " " + icon
                        col1 = col1.replace(icon, "").strip()
                
                col1 = col1.strip()
                if col1.endswith('/'): col1 = col1[:-1].strip()
                
                new_col1 = f"{col1} / \\textit{{{found_iast}}}{icons}"
                parts[0] = f" {new_col1} "
                updated_rows.append("&".join(parts))
                idx += num_words
                updated_count += 1
                continue
        
        updated_rows.append(row)
    
    if updated_count > 0:
        new_table_text = "\\\\".join(updated_rows)
        return content.replace(table_text, new_table_text), True
    return content, False

def main():
    base_dir = "sections"
    files = [f for f in os.listdir(base_dir) if f.endswith(".tex") and (f.startswith("chaupai") or f.startswith("doha") or f == "concluding_doha.tex")]
    
    # Simple natural sort
    def extract_num(s):
        m = re.search(r'\d+', s)
        return int(m.group()) if m else 0
    files.sort(key=extract_num)
    
    for filename in files:
        filepath = os.path.join(base_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        iast_words = extract_iast_words(content)
        if not iast_words:
            print(f"Skipping {filename}: No IAST words found")
            continue
            
        new_content, success = update_table(content, iast_words)
        if success:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {filename}")
        else:
            print(f"No changes for {filename}")

if __name__ == "__main__":
    main()
