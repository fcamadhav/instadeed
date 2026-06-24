with open('test_script.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

import re
matches = [m.start() for m in re.finditer("builder", content, re.IGNORECASE)]
print(f"Found 'builder' {len(matches)} times.")
for idx in matches[:10]:
    print(f"  Context: {repr(content[idx-30:idx+50])}")
