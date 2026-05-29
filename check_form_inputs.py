with open('test_script.jsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if "NoidaTransferForm" in line or (idx+1 >= 254 and idx+1 <= 512):
        if "label=" in line or "name=" in line:
            print(f"Line {idx+1}: {line.strip()}")
