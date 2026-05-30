import sys

# Ensure stdout uses UTF-8 if possible
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

with open('test_script.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

pos = content.find("DOCUMENT 5: Transfer Memo (TM) Application Form")
if pos == -1:
    print("DOCUMENT 5 string not found")
    exit()

# Print 1000 characters after pos
print("Block preview:")
print(content[pos:pos+1000])

print("\n--- Search for 'paper-page' after pos ---")
idx = pos
for _ in range(30):
    idx = content.find("paper-page", idx)
    if idx == -1:
        break
    line_num = content.count('\n', 0, idx) + 1
    # print the line
    line_start = content.rfind('\n', 0, idx) + 1
    line_end = content.find('\n', idx)
    print(f"Line {line_num}: {content[line_start:line_end].strip()}")
    idx += len("paper-page")
