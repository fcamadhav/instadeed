import re

def find_unannotated_variables(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Look for {dataObj.fieldName} where it is NOT inside <Var>...</Var>
    # Since we want to search lines between 4200 and 7000 (where templates are)
    pattern = re.compile(r'{(rentData|atsData|mutationData|gnidaData|tmAppData|tm48Data|noidaTransferData|gnidaRegistryData|gnidaPtmData|ecommTCData|ecommPPData|ecommRPData|regData)\.([a-zA-Z0-9_]+)}')
    
    print("Searching for unannotated variables in templates...")
    for idx in range(4200, min(7000, len(lines))):
        line = lines[idx]
        for match in pattern.finditer(line):
            # Check if this line also has <Var or if the match is wrapped in <Var
            # A simple heuristic: check if <Var is on the same line, or we can look closely
            if '<Var' not in line:
                print(f"Line {idx+1}: {line.strip()}")

if __name__ == '__main__':
    find_unannotated_variables('Madhav_Drafting_Hub.html')
