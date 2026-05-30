with open('test_script.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

import re

# Find occurrences of TM_APP or GNIDA_PACKAGE in rendering logic
matches = [m.start() for m in re.finditer(r"activeTab === 'TM_APP'", content)]
print("TM_APP occurrences in test_script.jsx:")
for idx in matches:
    print(f"Index {idx}: {repr(content[idx-100:idx+250])}")
    print("-" * 50)
