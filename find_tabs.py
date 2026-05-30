import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('test_script.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Let's search for some keys
search_terms = ["activeTab", "sidebar", "aside", "navigation", "Document Select", "Document Type", "select", "Document Options"]

for term in search_terms:
    pos = 0
    count = 0
    while True:
        pos = content.find(term, pos)
        if pos == -1:
            break
        count += 1
        pos += len(term)
    print(f"Term '{term}': {count} occurrences")

# Find where the sidebar container or navigation tabs are defined
# We can search for activeTab definition like const [activeTab,
pos = content.find("useState(")
while pos != -1:
    line_start = content.rfind('\n', 0, pos) + 1
    line_end = content.find('\n', pos)
    print("useState line:", content[line_start:line_end].strip())
    pos = content.find("useState(", pos + 9)
