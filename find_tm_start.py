with open('test_script.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

import re
matches = [m.start() for m in re.finditer(r"activeTab === 'TM_APP' \|\| activeTab === 'GNIDA_PACKAGE'", content)]
print("Matches found:", len(matches))
for idx in matches:
    line_num = content.count('\n', 0, idx) + 1
    print(f"Line {line_num}:")
    print(content[idx:idx+800])
    print("-" * 80)
