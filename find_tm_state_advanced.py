with open('test_script.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

import re
matches = [m.start() for m in re.finditer(r"tmAppData|tmData|defaultTm", content, re.IGNORECASE)]
print("Matches found:", len(matches))
for idx in matches[:15]:
    line_num = content.count('\n', 0, idx) + 1
    print(f"Line {line_num}: {repr(content[idx-30:idx+150])}")
