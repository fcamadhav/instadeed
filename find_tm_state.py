with open('test_script.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

import re
matches = [m.start() for m in re.finditer(r"tmAppData", content)]
print("tmAppData count:", len(matches))
# find where it is defined, e.g. const defaultTmAppData = or similar
pos = content.find("defaultTmAppData")
if pos != -1:
    print("Found defaultTmAppData at line:", content.count('\n', 0, pos) + 1)
    print(content[pos:pos+1500])
else:
    # search for tmAppData state hook, e.g. useState
    pos_state = content.find("useState")
    print("useState occurrences context:")
    pos_state = 0
    for _ in range(5):
        pos_state = content.find("useState", pos_state)
        if pos_state == -1:
            break
        print(content[pos_state:pos_state+150])
        pos_state += len("useState")
