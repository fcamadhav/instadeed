with open('test_script.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

import re
# Look for libraries or print handlers
keywords = ["pdf", "download", "print", "window.print", "jsPDF", "html2pdf"]
for kw in keywords:
    matches = [m.start() for m in re.finditer(kw, content, re.IGNORECASE)]
    print(f"Keyword '{kw}' found {len(matches)} times.")
    if matches:
        print("First few matches context:")
        for idx in matches[:5]:
            print(f"  Index {idx}: {repr(content[idx-30:idx+50])}")
