import re

def run_replacements(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern 1
    p1 = re.compile(r'<Var>{(rentData|atsData|mutationData|gnidaData|tmAppData|tm48Data|noidaTransferData|gnidaRegistryData|gnidaPtmData|ecommTCData|ecommPPData|ecommRPData)\.([a-zA-Z0-9_]+)(\s*\|\|[^}]+)?}</Var>')
    content, count1 = p1.subn(r'<Var name="\2">{\1.\2\3}</Var>', content)
    print(f"Substituted Pattern 1: {count1} times")

    # Pattern 2
    p2 = re.compile(r'<Var>{([a-zA-Z0-9_]+)\((rentData|atsData|mutationData|gnidaData|tmAppData|tm48Data|noidaTransferData|gnidaRegistryData|gnidaPtmData|ecommTCData|ecommPPData|ecommRPData)\.([a-zA-Z0-9_]+)\)}</Var>')
    content, count2 = p2.subn(r'<Var name="\3">{\1(\2.\3)}</Var>', content)
    print(f"Substituted Pattern 2: {count2} times")

    # Specific manual replacements
    replacements = {
        "<Var>{agreementDay}</Var>": "<Var name=\"agreementDate\">{agreementDay}</Var>",
        "<Var>{agreementMonthYear}</Var>": "<Var name=\"agreementDate\">{agreementMonthYear}</Var>",
        "<Var>{rentInWords || '________________________'}</Var>": "<Var name=\"rentAmount\">{rentInWords || '________________________'}</Var>",
        "<Var>{advanceInWords || '________________________'}</Var>": "<Var name=\"advanceRent\">{advanceInWords || '________________________'}</Var>",
        "<Var>{securityInWords || '________________________'}</Var>": "<Var name=\"securityDeposit\">{securityInWords || '________________________'}</Var>",
        "<Var>{formattedPaymentDay || '____'}</Var>": "<Var name=\"paymentDay\">{formattedPaymentDay || '____'}</Var>",
    }

    count3 = 0
    for pattern, repl in replacements.items():
        if pattern in content:
            content = content.replace(pattern, repl)
            count3 += 1

    print(f"Substituted manual patterns: {count3} types")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    run_replacements('Madhav_Drafting_Hub.html')
