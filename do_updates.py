import os
import re

print("Starting IAST update process...")

def clean_txt(t):
    # Basic cleaning for mapping
    return t.replace('।', '').replace('॥', '').replace('|', '').replace('||', '').replace(',', '').replace('.', '').strip().lower()

def get_mapping(content):
    # Extract Devanagari and IAST words from the verse section
    deva_matches = re.findall(r'\\deva\{([^\}]+)\}', content)
    iast_matches = re.findall(r'\\textit\{([^}]+)\}', content)
    
    deva_words = []
    for m in deva_matches:
        if len(m.split()) > 1 or '।' in m:
            deva_words.extend(clean_txt(m).split())
            
    iast_words = []
    for m in iast_matches:
        if '|' in m or '||' in m:
            iast_words.extend(clean_txt(m).split())
            
    mapping = []
    for d, i in zip(deva_words, iast_words):
        mapping.append((d, i))
    return mapping

def update_file(path):
    print(f"  Processing {path}...")
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    mapping = get_mapping(content)
    if not mapping:
        print(f"    Failed to find verse mapping in {path}")
        return

    table_pattern = re.compile(r'(\\begin\{tabularx\}.*?\\end\{tabularx\})', re.DOTALL)
    match = table_pattern.search(content)
    if not match:
        print(f"    No table found in {path}")
        return
    table_text = match.group(1)
    
    rows = table_text.split('\\\\')
    new_rows = []
    map_idx = 0
    updated_count = 0
    
    for row in rows:
        if '&' not in row or 'Awadhi' in row or 'midrule' in row:
            new_rows.append(row); continue
        
        parts = row.split('&')
        col1 = parts[0].strip()
        
        if '\\deva' in col1 and '\\telu' in col1 and '\\textit' not in col1:
            deva_match = re.search(r'\\deva\{([^\}]+)\}', col1)
            if deva_match:
                row_deva_words = clean_txt(deva_match.group(1)).split()
                
                # Find matching IAST words
                found_iast = []
                temp_idx = map_idx
                while temp_idx < len(mapping):
                    match_ok = True
                    for k in range(len(row_deva_words)):
                        if temp_idx + k >= len(mapping) or mapping[temp_idx + k][0] != row_deva_words[k]:
                            match_ok = False
                            break
                    if match_ok:
                        found_iast = [mapping[temp_idx + k][1] for k in range(len(row_deva_words))]
                        map_idx = temp_idx + len(row_deva_words)
                        break
                    temp_idx += 1
                
                if found_iast:
                    iast_str = " ".join(found_iast)
                    # Extract icon
                    icon = ""
                    for i in ['\\gotchaicon', '\\glossaryicon']:
                        if i in col1: icon = " " + i; col1 = col1.replace(i, "").strip()
                    
                    col1 = col1.strip().rstrip('/')
                    parts[0] = f" {col1} / \\textit{{{iast_str}}}{icon} "
                    updated_rows = "&".join(parts) # Wait, this should be row replacement
                    new_rows.append("&".join(parts))
                    updated_count += 1
                    continue
        new_rows.append(row)
    
    if updated_count > 0:
        new_table = "\\\\".join(new_rows)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content.replace(table_text, new_table))
        print(f"    Updated {updated_count} rows in {path}")
    else:
        print(f"    No rows updated in {path}")

def main():
    folder = "sections"
    files = sorted([f for f in os.listdir(folder) if f.endswith(".tex") and ("chaupai" in f or "doha" in f)])
    for f in files:
        update_file(os.path.join(folder, f))
    print("Process complete.")

if __name__ == "__main__":
    main()
