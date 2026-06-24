with open('test_script.jsx.bak', 'r', encoding='utf-8') as f:
    bak_content = f.read()

with open('test_script.jsx', 'r', encoding='utf-8') as f:
    curr_content = f.read()

import re
bak_matches = [m.start() for m in re.finditer(r"activeTab === 'TM_APP'", bak_content)]
curr_matches = [m.start() for m in re.finditer(r"activeTab === 'TM_APP'", curr_content)]

print("Bak activeTab === 'TM_APP' matches:")
for idx in bak_matches:
    line = bak_content.count('\n', 0, idx) + 1
    print(f"Line {line}: {repr(bak_content[idx:idx+150])}")

print("\nCurr activeTab === 'TM_APP' matches:")
for idx in curr_matches:
    line = curr_content.count('\n', 0, idx) + 1
    print(f"Line {line}: {repr(curr_content[idx:idx+150])}")
