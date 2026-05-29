with open('test_script.jsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if "const Var" in line:
        print(f"Line {idx+1}: {line.strip()}")
        # print next 25 lines
        for i in range(idx+1, idx+26):
            print(f"{i+1}: {lines[i].strip()}")
