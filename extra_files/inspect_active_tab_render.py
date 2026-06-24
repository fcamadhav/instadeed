with open('test_script.jsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(6160, 6210):
    line_content = lines[i-1].rstrip('\r\n')
    safe_content = line_content.encode('ascii', errors='replace').decode('ascii')
    print(f"{i}: {safe_content}")
