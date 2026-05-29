import re

def apply_replace(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Pattern: match {data.field} not preceded by = or $
    pattern = re.compile(r'(?<![=$]){(rentData|atsData|mutationData|gnidaData|tmAppData|tm48Data|noidaTransferData|gnidaRegistryData|gnidaPtmData|ecommTCData|ecommPPData|ecommRPData|regData)\.([a-zA-Z0-9_]+)(\s*\|\|[^}]+)?}')

    change_count = 0
    # Process lines in the template range
    for idx in range(len(lines)):
        if 4211 <= idx <= 7074:
            new_line, n = pattern.subn(r'<Var name="\2">{\1.\2\3}</Var>', lines[idx])
            if n > 0:
                change_count += n
                lines[idx] = new_line

    print(f"Applied {change_count} replacements inside document templates.")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

if __name__ == '__main__':
    apply_replace('Madhav_Drafting_Hub.html')
