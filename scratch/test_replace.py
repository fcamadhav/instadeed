import re

def test_replace(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Pattern: match {data.field} not preceded by = or $
    pattern = re.compile(r'(?<![=$]){(rentData|atsData|mutationData|gnidaData|tmAppData|tm48Data|noidaTransferData|gnidaRegistryData|gnidaPtmData|ecommTCData|ecommPPData|ecommRPData|regData)\.([a-zA-Z0-9_]+)(\s*\|\|[^}]+)?}')

    # Process lines in the template range
    modified_lines = []
    change_count = 0
    
    # Template range starts around index 4211 (line 4212) to index 7074 (line 7075)
    for idx, line in enumerate(lines):
        if 4211 <= idx <= 7074:
            # Replace
            new_line, n = pattern.subn(r'<Var name="\2">{\1.\2\3}</Var>', line)
            if n > 0:
                change_count += n
                modified_lines.append((idx + 1, line.strip(), new_line.strip()))
        else:
            pass

    print(f"Total replacements that will be applied: {change_count}")
    print("\nSample replacements:")
    for idx, old, new in modified_lines[:15]:
        print(f"Line {idx}:")
        print(f"  Old: {old}")
        print(f"  New: {new}")

if __name__ == '__main__':
    test_replace('Madhav_Drafting_Hub.html')
