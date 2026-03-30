import os
import re

d = '/Users/awesome/edu/H40/sections'
for f in os.listdir(d):
    if not f.endswith('.tex'): continue
    path = os.path.join(d, f)
    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # We find every tabularx block.
    # Pattern to find tabularx preamble and its contents: 
    # \begin{tabularx}{...}{|...|}
    # \hline
    # CONTENT
    # \hline
    tables = re.findall(r'\\begin\{tabularx\}\{.*?\}\{(.*?)\}\s*\\hline\s*(.*?)\s*\\hline', content, flags=re.DOTALL)
    
    for table_idx, (preamble, inner_content) in enumerate(tables):
        # 1. Parse preamble to extract the written \hsize multipliers
        hsize_matches = re.findall(r'\\hsize=([0-9\.]+)\\hsize\}X', preamble)
        written_hsizes = [float(x) for x in hsize_matches]
        columns_count = len(written_hsizes)
        
        # 2. Parse inner_content to extract the literal matra count numbers: "(x)"
        matra_matches = re.findall(r'\(\s*(\d+)\s*\)', inner_content)
        literal_matras = [int(x) for x in matra_matches]
        
        if not literal_matras:
            continue
            
        total_matras = sum(literal_matras)
        
        if len(literal_matras) != columns_count:
            print(f"[ERR] {f} Table {table_idx}: Columns {columns_count} != Matra Numbers {len(literal_matras)}")
            continue
            
        # 3. Calculate what the mathematically PERFECT hsizes should be
        perfect_hsizes = []
        for matra in literal_matras:
            perfect_hsize = (matra / total_matras) * columns_count
            perfect_hsizes.append(perfect_hsize)
            
        # 4. Compare
        mismatch = False
        for i in range(columns_count):
            if abs(written_hsizes[i] - perfect_hsizes[i]) > 0.01:
                mismatch = True
                
        if mismatch:
            print(f"--- FLAW DETECTED IN {f} Table {table_idx+1} ---")
            print(f"Literal Matras array: {literal_matras} = Total {total_matras}")
            print(f"Expected \\hsizes: {[round(x,4) for x in perfect_hsizes]}")
            print(f"Current \\hsizes:  {written_hsizes}")

