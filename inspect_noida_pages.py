with open('test_script.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Locate NoidaTransferPreview or activeTab === 'NOIDA_TRANSFER'
pos = content.find("activeTab === 'NOIDA_TRANSFER'")
if pos == -1:
    print("NOIDA_TRANSFER tab not found")
    exit()

print("Searching for pages in NOIDA_TRANSFER preview section...")
import re

# Let's search for {/* PAGE X: ... */} comment and print them, and find the next footer number
page_pattern = re.compile(r'\{\s*\/\*\s*(PAGE\s+\d+:[^*]*)\*\/\s*\}')
matches = list(page_pattern.finditer(content, pos))

for i, match in enumerate(matches):
    start = match.start()
    title = match.group(1).strip()
    
    # Let's find the footer page number for this page
    # It should be absolute bottom-4 or bottom-6 div
    next_page_start = matches[i+1].start() if i+1 < len(matches) else len(content)
    page_content = content[start:next_page_start]
    
    footer_match = re.search(r'Page\s+(\d+)', page_content)
    footer_num = footer_match.group(1) if footer_match else "Not found"
    
    print(f"Title: '{title}'")
    print(f"  First 200 chars of content: {repr(page_content[:200])}")
    print(f"  Extracted page number from footer: {footer_num}")
