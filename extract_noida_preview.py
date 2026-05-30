with open('test_script.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

import re

# Find start and end of activeTab === 'NOIDA_TRANSFER' rendering block
# Let's search for "activeTab === 'NOIDA_TRANSFER' &&" in test_script.jsx
pos = content.find("activeTab === 'NOIDA_TRANSFER' &&")
if pos == -1:
    print("NOIDA_TRANSFER block not found")
    exit()

print("Found NOIDA_TRANSFER at index:", pos)
# Let's find where KYA or next tab starts to get the boundary of the NOIDA_TRANSFER block
end_pos = content.find("activeTab === 'KYA'", pos)
if end_pos == -1:
    end_pos = len(content)

noida_block = content[pos:end_pos]

# Let's count 'paper-page' occurrences
pages = re.findall(r'paper-page', noida_block)
print(f"Number of paper-page elements in NOIDA_TRANSFER block: {len(pages)}")

# Print lines where paper-page is defined to see the classes and conditionals
idx = 0
for m in re.finditer(r'paper-page', noida_block):
    start = m.start()
    line_start = noida_block.rfind('\n', 0, start) + 1
    line_end = noida_block.find('\n', start)
    print(f"Page {idx+1}: {noida_block[line_start:line_end].strip()}")
    idx += 1
