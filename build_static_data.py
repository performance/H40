import os
import re
import json

LATEX_DIR = '/Users/awesome/edu/H40/sections'
OUTPUT_DIR = '/Users/awesome/edu/H40/web/src/lib/data'

def clean_latex_macros(text):
    # Strip simple diacritics first so they don't break the brace matching loop
    text = re.sub(r'\\[=~\.\^]\{([a-zA-Z])\}', r'\1', text)
    
    # Handle nested macros from the inside out using a loop
    prev = ""
    while text != prev:
        prev = text
        text = re.sub(r'\\textbf\{([^{}]+)\}', r'**\1**', text)
        text = re.sub(r'\\textit\{([^{}]+)\}', r'*\1*', text)
        text = re.sub(r'\\href\{([^{}]+)\}\{([^{}]+)\}', r'[\2](\1)', text)
        # Handle \textcolor{color}{text} where neither parameter contains nested braces
        text = re.sub(r'\\textcolor\{([^{}]+)\}\{([^{}]+)\}', r'\2', text)
        text = re.sub(r'\\(?:deva|telu|guru|laghu)\{([^{}]+)\}', r'\1', text)

    # Strip any remaining un-nested or malformed macros
    text = re.sub(r'\\(?:deva|telu|guru|laghu)\{([^}]*)\}', r'\1', text)
    text = re.sub(r'\\textbf\{([^}]*)\}', r'**\1**', text)
    text = re.sub(r'\\textit\{([^}]*)\}', r'*\1*', text)
    
    # Replace LaTeX commands with empty strings or equivalents
    text = re.sub(r'\\[a-zA-Z]+icon\b', '', text)
    text = re.sub(r'\\addcontentsline\{[^}]*\}\{[^}]*\}\{[^}]*\}', '', text)
    text = re.sub(r'\\par', '\n', text)
    text = re.sub(r'\\newline', ' ', text)
    text = re.sub(r'\\vspace\{[^}]*\}', '\n', text)
    text = re.sub(r'\\newpage', '', text)
    text = re.sub(r'\\phantomsection', '', text)
    text = re.sub(r'\\textcolor\{[^}]*\}\{([^}]*)\}', r'\1', text)
    text = re.sub(r'\\hr\b', '---', text)
    text = re.sub(r'\\rightarrow', '→', text)
    text = re.sub(r'\$', '', text)
    
    # Clean up excess whitespace created by stripping commands
    lines = text.split('\n')
    cleaned_lines = [l.strip() for l in lines]
    # Remove multiple consecutive blank lines
    text = '\n'.join([l for l in cleaned_lines if l])
    return text

def parse_preface():
    filepath = os.path.join(LATEX_DIR, 'preface.tex')
    with open(filepath, 'r') as f:
        content = f.read()
        
    # Convert section/subsection to Markdown headers
    content = re.sub(r'\\section\*?\{([^}]*)\}', r'# \1\n', content)
    content = re.sub(r'\\subsection\*?\{([^}]*)\}', r'## \1\n', content)
    content = re.sub(r'\\subsubsection\*?\{([^}]*)\}', r'### \1\n', content)
    
    # Convert itemize and enumerate to Markdown lists
    content = re.sub(r'\\begin\{itemize\}', '', content)
    content = re.sub(r'\\end\{itemize\}', '', content)
    content = re.sub(r'\\begin\{enumerate\}', '', content)
    content = re.sub(r'\\end\{enumerate\}', '', content)
    content = re.sub(r'\\begin\{description\}', '', content)
    content = re.sub(r'\\end\{description\}', '', content)
    
    # Handle \item
    content = re.sub(r'\\item\s*\[(.*?)\]', r'- **\1**', content)
    content = re.sub(r'\\item', r'- ', content)
    
    # Strip tcolorbox
    content = re.sub(r'\\begin\{tcolorbox\}\[[^]]*\](?:\[title=.*?\])?', '---', content)
    content = re.sub(r'\\begin\{tcolorbox\}[^\n]*', '---', content)
    content = re.sub(r'\\end\{tcolorbox\}', '---', content)
    
    # Strip comments
    content = re.sub(r'(?m)^%.*$', '', content)
    
    md_content = clean_latex_macros(content)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(os.path.join(OUTPUT_DIR, 'intro.md'), 'w') as f:
        f.write(md_content)
        
    print(f"Parsed preface into intro.md")

def parse_glossary():
    filepath = os.path.join(LATEX_DIR, 'glossary.tex')
    with open(filepath, 'r') as f:
        content = f.read()
        
    entries = []
    sections = content.split('\\subsection*{')
    
    for section in sections[1:]:
        title_match = re.search(r'\\textbf\{\d+\.\s*(.*?)\s*\((.*?)\)\}', section)
        term = ""
        transliteration = ""
        if title_match:
            term = title_match.group(1).strip()
            transliteration = title_match.group(2).strip()
            
        # The remainder of the text before the table
        section_lines = section.split('\n', 1)
        body_raw = section_lines[1] if len(section_lines) > 1 else ""
        body_match = re.search(r'(.*?)\\begin\{table\}', body_raw, re.DOTALL)
        body = body_match.group(1).strip() if body_match else ""
        body_cleaned = clean_latex_macros(body)
        
        # Parse table items
        items = []
        table_body_match = re.search(r'\\midrule(.*?)\\bottomrule', section, re.DOTALL)
        if table_body_match:
            rows = table_body_match.group(1).strip().split('\\\\')
            for row in rows:
                if not row.strip(): continue
                cols = row.split('&')
                if len(cols) >= 3:
                    item_name = clean_latex_macros(cols[0])
                    item_sanskrit = clean_latex_macros(cols[1])
                    item_desc = clean_latex_macros(cols[2])
                    items.append({
                        "name": item_name,
                        "sanskrit": item_sanskrit,
                        "description": item_desc
                    })
        
        if term:
            entries.append({
                "category": term,
                "sanskrit_name": transliteration,
                "description": body_cleaned,
                "items": items
            })
            
    with open(os.path.join(OUTPUT_DIR, 'glossary.json'), 'w', encoding='utf-8') as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)
        
    print(f"Parsed {len(entries)} glossary categories into glossary.json")

def parse_references():
    filepath = os.path.join(LATEX_DIR, 'references.tex')
    with open(filepath, 'r') as f:
        content = f.read()
        
    # Convert section/subsection to Markdown headers
    content = re.sub(r'\\section\*?\{([^}]*)\}', r'# \1\n', content)
    content = re.sub(r'\\subsection\*?\{([^}]*)\}', r'### \1\n', content)
    
    # Convert itemize to Markdown lists
    content = re.sub(r'\\begin\{itemize\}', '', content)
    content = re.sub(r'\\end\{itemize\}', '', content)
    
    # Handle \item
    content = re.sub(r'\\item', r'- ', content)
    
    # Strip comments
    content = re.sub(r'(?m)^%.*$', '', content)
    
    md_content = clean_latex_macros(content)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(os.path.join(OUTPUT_DIR, 'references.md'), 'w') as f:
        f.write(md_content)
        
    print(f"Parsed references into references.md")

if __name__ == '__main__':
    parse_preface()
    parse_glossary()
    parse_references()
