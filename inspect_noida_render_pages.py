with open('test_script.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

pos = content.find("activeTab === 'NOIDA_TRANSFER' && (() => {")
if pos == -1:
    print("NOIDA_TRANSFER block not found")
    exit()

end_pos = content.find("})()}", pos)
if end_pos == -1:
    end_pos = len(content)

subcontent = content[pos:end_pos]
import re
# Find all occurrences of paper-page or comments inside subcontent
matches = re.finditer(r'paper-page', subcontent)
print("paper-page instances in NOIDA_TRANSFER render block:")
for m in matches:
    idx = pos + m.start()
    line_num = content.count('\n', 0, idx) + 1
    # print the line
    line_start = content.rfind('\n', 0, idx) + 1
    line_end = content.find('\n', idx)
    print(f"Line {line_num}: {content[line_start:line_end].strip()}")
