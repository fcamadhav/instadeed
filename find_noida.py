import sys

with open('test_script.jsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("Line 2670 to 2720:")
for i in range(2670, min(2720, len(lines))):
    line_content = lines[i-1].rstrip('\r\n')
    safe_content = line_content.encode('ascii', errors='replace').decode('ascii')
    print(f"{i}: {safe_content}")
