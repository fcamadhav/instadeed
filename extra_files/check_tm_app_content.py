with open('test_script.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

pos = content.find("activeTab === 'TM_APP' || activeTab === 'GNIDA_PACKAGE'")
if pos == -1:
    print("GNIDA TM block not found")
    exit()

end_pos = content.find("activeTab === 'KYA'", pos)
if end_pos == -1:
    end_pos = len(content)

subcontent = content[pos:end_pos]

import re
matches = list(re.finditer(r'paper-page', subcontent))

with open('tm_app_code_extracted.txt', 'w', encoding='utf-8') as out:
    for i, m in enumerate(matches):
        start = m.start()
        end = matches[i+1].start() if i+1 < len(matches) else len(subcontent)
        page_text = subcontent[start:end]
        
        # Remove tags and formatting to get raw text
        clean_text = re.sub(r'<[^<]+?>', ' ', page_text)
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
        
        out.write(f"--- PAGE {i+1} ---\n")
        out.write(clean_text + "\n\n")

print("Dumped TM_APP code text to tm_app_code_extracted.txt")
