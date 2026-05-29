import sys

with open('test_script.jsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

start = 254
end = 254
brace_count = 0
found_start = False

for idx in range(254, len(lines)):
    line = lines[idx-1]
    if "const NoidaTransferForm" in line:
        start = idx
        found_start = True
    if found_start:
        brace_count += line.count('{') - line.count('}')
        if brace_count == 0 and idx > start:
            end = idx
            break

print(f"NoidaTransferForm line range: {start} to {end}")
for i in range(start, end + 1):
    line_content = lines[i-1].rstrip('\r\n')
    safe_content = line_content.encode('ascii', errors='replace').decode('ascii')
    print(f"{i}: {safe_content}")
