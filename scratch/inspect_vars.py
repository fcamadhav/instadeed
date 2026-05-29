import re

def inspect_var_tags(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all Var tags
    pattern = re.compile(r'<Var name="([^"]+)">([^<]+)</Var>')
    matches = list(pattern.finditer(content))
    print(f"Total Var tags: {len(matches)}")
    
    # We want to find cases where the content contains invalid characters like '&&', '?', 'map', etc.
    invalid_count = 0
    for m in matches:
        name = m.group(1)
        val = m.group(2)
        if any(char in val for char in ['&&', '?', 'map', '=>', 'import', 'const', 'let', 'function']):
            print(f"SUSPICIOUS VAR: {m.group(0)}")
            invalid_count += 1
            
    print(f"Total suspicious/invalid Var tags: {invalid_count}")

if __name__ == '__main__':
    inspect_var_tags('Madhav_Drafting_Hub.html')
