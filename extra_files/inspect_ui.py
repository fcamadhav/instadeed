import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('test_script.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Let's search for occurrences of 'activeTab ===' or tabs list
pos = content.find("activeTab === 'HOME'")
while pos != -1:
    line_start = content.rfind('\n', 0, pos) + 1
    line_end = content.find('\n', pos)
    print(f"Position {pos}: {content[line_start:line_end].strip()}")
    # Let's print 300 characters around this pos
    print("--- CONTEXT ---")
    print(content[pos-100:pos+300])
    print("===============")
    pos = content.find("activeTab === 'HOME'", pos + 20)
