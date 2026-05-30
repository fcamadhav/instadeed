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
print("Total pages in GNIDA TM:", len(matches))

for i, m in enumerate(matches):
    start = m.start()
    end = matches[i+1].start() if i+1 < len(matches) else len(subcontent)
    page_text = subcontent[start:end]
    
    print(f"\n--- PAGE {i+1} ---")
    headings = re.findall(r'<h[1-6][^>]*>(.*?)</h[1-6]>', page_text)
    if headings:
        print("  Headings:", [re.sub('<[^<]+?>', '', h).strip() for h in headings])
    else:
        clean_text = re.sub('<[^<]+?>', ' ', page_text)
        clean_text = re.sub('\s+', ' ', clean_text).strip()
        print("  Text snippet:", clean_text[:200])
