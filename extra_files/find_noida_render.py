with open('test_script.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

import re
matches = [m.start() for m in re.finditer(r"activeTab === 'NOIDA_TRANSFER'", content)]
print("NOIDA_TRANSFER occurrences count:", len(matches))
for idx in matches:
    line_num = content.count('\n', 0, idx) + 1
    print(f"Line {line_num}:")
    context = content[idx:idx+400]
    print(repr(context))
    print("-" * 80)
