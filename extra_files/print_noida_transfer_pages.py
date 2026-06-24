with open('test_script.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

pos = content.find("activeTab === 'NOIDA_TRANSFER'")
if pos == -1:
    print("NOIDA_TRANSFER tab not found")
    exit()

# We know the Noida Transfer section ends before the activeTab === 'GNIDA_REGISTRY' or another major tab block.
# Let's search from pos up to 100000 characters
block = content[pos:pos+100000]

import re
# Match any { /* PAGE X: ... */ } or {/* PAGE X: ... */}
matches = re.findall(r'\{\s*/\*\s*(PAGE\s+\d+:[^*]*)\s*\*/\s*\}', block)
print("Found pages:")
for m in matches:
    print(" -", m.strip())
