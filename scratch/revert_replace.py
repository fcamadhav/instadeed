import re

def revert_replace(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern: match <Var name="...">...</Var>
    # Group 1: field name in name attribute
    # Group 2: data object name (e.g. rentData, atsData)
    # Group 3: field name in expression
    # Group 4: optional fallback expression
    pattern = re.compile(r'<Var name="([a-zA-Z0-9_]+)">{(rentData|atsData|mutationData|gnidaData|tmAppData|tm48Data|noidaTransferData|gnidaRegistryData|gnidaPtmData|ecommTCData|ecommPPData|ecommRPData|regData)\.([a-zA-Z0-9_]+)(\s*\|\|[^}]+)?}</Var>')

    new_content, count = pattern.subn(r'{\2.\3\4}', content)
    print(f"Reverted {count} Var tag wrappers.")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

if __name__ == '__main__':
    revert_replace('Madhav_Drafting_Hub.html')
