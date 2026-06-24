import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('test_script.jsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Print lines where activeTab is set inside the sidebar (around lines 3800 to 4550)
for i in range(3780, 4550):
    line = lines[i-1]
    if 'setActiveTab' in line or 'activeAuthority' in line or 'Document Select' in line or 'select' in line:
        print(f"Line {i}: {line.strip()}")
