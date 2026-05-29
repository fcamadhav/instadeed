import re

def annotate_vars(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Define regexes for various patterns of variables inside Var tags
    # Pattern 1: <Var>{dataObj.fieldName || 'default'}</Var>
    # Group 1: data object name (e.g., rentData)
    # Group 2: field name (e.g., landlordName)
    # Group 3: optional fallback/OR content
    p1 = re.compile(r'<Var>{(rentData|atsData|mutationData|gnidaData|tmAppData|tm48Data|noidaTransferData|gnidaRegistryData|gnidaPtmData|ecommTCData|ecommPPData|ecommRPData)\.([a-zA-Z0-9_]+)(\s*\|\|[^}]+)?}</Var>')

    # Pattern 2: <Var>{helperFunc(dataObj.fieldName)}</Var>
    # Group 1: helper function (e.g., formatPan)
    # Group 2: data object name (e.g., atsData)
    # Group 3: field name (e.g., seller1Pan)
    p2 = re.compile(r'<Var>{([a-zA-Z0-9_]+)\((rentData|atsData|mutationData|gnidaData|tmAppData|tm48Data|noidaTransferData|gnidaRegistryData|gnidaPtmData|ecommTCData|ecommPPData|ecommRPData)\.([a-zA-Z0-9_]+)\)}</Var>')

    # Pattern 3: <Var>Rs.{dataObj.fieldName}/- (Rupees {dataObj.fieldWords} Only.)</Var>
    # Let's match customized composite Var tags individually or refine
    
    # Let's see how many matches we get
    matches1 = p1.findall(content)
    matches2 = p2.findall(content)
    
    print(f"Pattern 1 matches: {len(matches1)}")
    for m in matches1[:10]:
        print("  P1:", m)
        
    print(f"Pattern 2 matches: {len(matches2)}")
    for m in matches2[:10]:
        print("  P2:", m)

if __name__ == '__main__':
    annotate_vars('Madhav_Drafting_Hub.html')
