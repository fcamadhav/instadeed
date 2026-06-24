import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('test_script.jsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("Printing lines 3780 to 4000:")
for i in range(3780, min(4000, len(lines))):
    line_content = lines[i-1].rstrip('\r\n')
    safe_content = line_content.encode('ascii', errors='replace').decode('ascii')
    print(f"{i}: {safe_content}")
