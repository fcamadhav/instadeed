import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('test_script.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

pos = content.find("const renderHomeDashboard")
if pos != -1:
    end_pos = content.find("const renderCrmDashboard", pos)
    if end_pos == -1:
        end_pos = pos + 5000
    with open('scratch/home_dashboard_code.txt', 'w', encoding='utf-8') as out:
        out.write(content[pos:end_pos])
    print(f"Extracted renderHomeDashboard from {pos} to {end_pos}")
else:
    print("renderHomeDashboard not found")
