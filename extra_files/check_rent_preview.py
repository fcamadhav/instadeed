with open('test_script.jsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if "landlordName" in line and idx + 1 > 4500:
        print(f"Line {idx+1}: {line.strip()}")
