with open('test_script.jsx.bak', 'r', encoding='utf-8') as f:
    bak_lines = f.readlines()

with open('test_script.jsx', 'r', encoding='utf-8') as f:
    curr_lines = f.readlines()

# Search for the block starting with Line 8075 in bak vs Line 8525 in curr
bak_start = 8074 # 0-indexed line 8075
curr_start = 8524 # 0-indexed line 8525

import difflib
diff = difflib.unified_diff(
    bak_lines[bak_start:bak_start+300],
    curr_lines[curr_start:curr_start+300],
    fromfile='test_script.jsx.bak',
    tofile='test_script.jsx'
)
with open('diff_output.txt', 'w', encoding='utf-8') as out:
    out.write(''.join(diff))
print("Diff written to diff_output.txt")
