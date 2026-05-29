import re

def dry_run_wrapping(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Match {data.field} NOT preceded by =
    # Group 1: data object name (e.g. rentData, atsData, regData)
    # Group 2: field name (e.g. landlordName)
    # Group 3: optional fallback/OR expression
    pattern = re.compile(r'(?<!=){(rentData|atsData|mutationData|gnidaData|tmAppData|tm48Data|noidaTransferData|gnidaRegistryData|gnidaPtmData|ecommTCData|ecommPPData|ecommRPData|regData)\.([a-zA-Z0-9_]+)(\s*\|\|[^}]+)?}')

    matches = list(pattern.finditer(content))
    print(f"Total matches found in text nodes: {len(matches)}")
    
    # Let's inspect the first 20 matches to verify
    for i, m in enumerate(matches[:20]):
        # Print matching substring and its line context
        start, end = m.span()
        # Find line number
        line_no = content.count('\n', 0, start) + 1
        line_content = content[start - 50: end + 50].replace('\n', ' ')
        print(f"Match {i+1} (Line {line_no}): ... {line_content} ...")

if __name__ == '__main__':
    dry_run_wrapping('Madhav_Drafting_Hub.html')
