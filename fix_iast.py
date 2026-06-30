import os
import re

def fix_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {path}: {e}")
        return False

    if '\\textit{' in content and '/ \\textit' in content:
        # Already updated? Check specifically in the tabularx
        return False

    # Get IAST verse
    iv = ""
    matches = re.findall(r'\\textit\{([^}]+)\}', content)
    for m in matches:
        if '|' in m or '||' in m:
            iv += " " + m
    if not iv: 
        # Fallback for concluding_doha
        if "concluding_doha" in path:
            for m in matches:
                if len(m.split()) > 3: iv = m; break
        else:
            return False
    
    iw = iv.lower().replace('|',' ').replace('||',' ').replace(',',' ').replace('.',' ').split()
    
    # Get Devanagari verse
    dv = ""
    matches = re.findall(r'\\deva\{([^\}]+)\}', content)
    for m in matches:
        if len(m.split()) > 1 or '।' in m or '॥' in m:
            dv += " " + m
    
    cleaned_dv = dv.replace('।', ' ').replace('॥', ' ').replace('|', ' ').replace('||', ' ').replace(',', ' ')
    dw = cleaned_dv.strip().lower().split()
    
    if len(dw) == 0 or len(iw) == 0: 
        return False
    
    # Mapping
    mapping = list(zip(dw, iw))
    
    # Find table
    m = re.search(r'\\begin\{tabularx\}.*?\\end\{tabularx\}', content, re.DOTALL)
    if not m: return False
    table = m.group(0)
    
    rows = table.split('\\\\')
    new_rows = []
    idx = 0
    updated = 0
    
    for row in rows:
        if '&' in row and '\\deva' in row and '\\telu' in row and '\\textit' not in row:
            dm = re.search(r'\\deva\{([^\}]+)\}', row)
            if dm:
                row_raw = dm.group(1).replace('।','').replace('॥','').replace('|','').replace('||','').strip().lower()
                row_dw = row_raw.split()
                
                found = []
                # Search for match in mapping
                for j in range(idx, len(mapping)):
                    if j < len(mapping) and mapping[j][0] == (row_dw[0] if row_dw else ""):
                        match_ok = True
                        for k in range(len(row_dw)):
                            if j+k >= len(mapping) or mapping[j+k][0] != row_dw[k]:
                                match_ok = False; break
                        if match_ok:
                            found = [mapping[j+k][1] for k in range(len(row_dw))]
                            idx = j + len(row_dw)
                            break
                
                if found:
                    iast_text = " ".join(found)
                    col1_match = re.search(r'^([^\&]+)\&', row.strip())
                    if col1_match:
                        col1 = col1_match.group(1).strip()
                        icons = ""
                        for ic in ['\\gotchaicon', '\\glossaryicon']:
                            if ic in col1: icons += " " + ic; col1 = col1.replace(ic, "").strip()
                        col1 = col1.rstrip('/') .strip()
                        new_col1 = f"{col1} / \\textit{{{iast_text}}}{icons} "
                        updated_row = row.replace(col1_match.group(1), new_col1)
                        new_rows.append(updated_row)
                        updated += 1
                        continue
        new_rows.append(row)
    
    if updated > 0:
        new_table = "\\\\".join(new_rows)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content.replace(table, new_table))
        print(f"Updated {path}")
        return True
    return False

def main():
    sections_dir = 'sections'
    files = sorted([f for f in os.listdir(sections_dir) if f.endswith('.tex') and ('chaupai' in f or 'doha' in f)])
    for f in files:
        fix_file(os.path.join(sections_dir, f))

if __name__ == "__main__":
    main()
