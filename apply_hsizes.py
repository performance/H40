import os
import re

d = '/Users/awesome/edu/H40/sections'
for f in os.listdir(d):
    if not f.endswith('.tex'): continue
    path = os.path.join(d, f)
    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    tables = re.findall(r'(\\begin\{tabularx\}\{.*?\}\{)(.*?)(\}\s*\\hline\s*(.*?)\s*\\hline)', content, flags=re.DOTALL)
    
    modified = False
    new_content = content
    
    for tbl in tables:
        preamble_start, preamble_cols, post_preamble, inner_content = tbl
        
        # parse inner literal numbers
        matra_matches = re.findall(r'\(\s*(\d+)\s*\)', inner_content)
        literal_matras = [int(x) for x in matra_matches]
        if not literal_matras: continue
        total_matras = sum(literal_matras)
        
        # parse written hsizes
        hsize_matches = re.findall(r'\\hsize=([0-9\.]+)\\hsize', preamble_cols)
        if len(hsize_matches) != len(literal_matras): continue
        
        written_hsizes = [float(x) for x in hsize_matches]
        columns_count = len(written_hsizes)
        
        perfect_hsizes = []
        mismatch = False
        for i, matra in enumerate(literal_matras):
            perfect_hsize = (matra / total_matras) * columns_count
            perfect_hsizes.append(perfect_hsize)
            if abs(written_hsizes[i] - perfect_hsize) > 0.01:
                mismatch = True
                
        if mismatch:
            new_cols = ""
            for h in perfect_hsizes:
                new_cols += f"|>{{\\centering\\arraybackslash\\hsize={h:.4f}\\hsize}}X"
            new_cols += "|"
            
            old_table_str = preamble_start + preamble_cols + post_preamble
            new_table_str = preamble_start + new_cols + post_preamble
            new_content = new_content.replace(old_table_str, new_table_str)
            modified = True
            
    if modified:
        with open(path, 'w', encoding='utf-8') as file:
            file.write(new_content)
        print(f"Patched geometric matrix in {f}")
