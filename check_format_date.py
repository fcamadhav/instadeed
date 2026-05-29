with open('test_script.jsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if "const formatDate" in line:
        print(f"Line {idx+1}: {line.strip()}")
        for i in range(idx+1, idx+15):
            print(f"{i+1}: {lines[i].strip()}")
