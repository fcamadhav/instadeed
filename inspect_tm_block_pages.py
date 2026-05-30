with open('test_script.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

pos = content.find("activeTab === 'TM_APP'")
if pos == -1:
    print("TM_APP tab not found")
    exit()

end_pos = content.find("activeTab === 'KYA'")
if end_pos == -1:
    end_pos = len(content)

tm_block = content[pos:end_pos]

import re
matches = re.finditer(r'paper-page', tm_block)
print("Found paper-page occurrences inside the TM block:")
for m in matches:
    # find the line number of this match in test_script.jsx
    idx = pos + m.start()
    line_num = content.count('\n', 0, idx) + 1
    # print the line
    line_start = content.rfind('\n', 0, idx) + 1
    line_end = content.find('\n', idx)
    print(f"Line {line_num}: {content[line_start:line_end].strip()}")
