import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('test_script.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

pos = content.find("function renderHomeDashboard")
if pos == -1:
    pos = content.find("const renderHomeDashboard")

if pos != -1:
    print(content[pos:pos+2000])
else:
    print("renderHomeDashboard not found")
