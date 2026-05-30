with open('test_script.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

idx = 783721
# Find the start of the enclosing activeTab rendering block
start_pos = content.rfind('activeTab ===', 0, idx)
# print 1000 characters before and 3000 characters after idx
print("=== GNIDA TM BLOCK ===")
print("Start position:", start_pos)
print(repr(content[start_pos:idx+1500]))
