with open('test_script.jsx', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'name="[^"]*Age"', text)
print("Age fields found in test_script.jsx:", matches)

# Also let's inspect the NoidaTransferForm code from line 300 to 520
print("\nForm inputs around Transferors & Transferees:")
lines = text.splitlines()
for idx, line in enumerate(lines):
    if idx + 1 >= 300 and idx + 1 <= 520:
        if "label=" in line or "name=" in line:
            print(f"{idx+1}: {line.strip()}")
