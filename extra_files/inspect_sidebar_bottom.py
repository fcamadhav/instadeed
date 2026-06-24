import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('test_script.jsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("Printing lines 4000 to 4550:")
for i in range(4000, min(4550, len(lines))):
    line_content = lines[i-1].rstrip('\r\n')
    safe_content = line_content.encode('ascii', errors='replace').decode('ascii')
    print(f"{i}: {safe_content}")
