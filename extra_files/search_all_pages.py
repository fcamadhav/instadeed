with open('test_script.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

import re

# Match any comment with 'PAGE' in it, including single-line and multi-line React comments
pattern = re.compile(r'\{\s*/\*\s*([^*]*?PAGE[^*]*?)\s*\*/\s*\}')
matches = pattern.finditer(content)

print("All PAGE comments in test_script.jsx:")
count = 0
for m in matches:
    count += 1
    idx = m.start()
    comment_text = m.group(1).strip()
    print(f"{count:02d}. Index {idx}: '{comment_text}'")
