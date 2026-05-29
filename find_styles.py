import os

def search_in_file(filename, query):
    if not os.path.exists(filename):
        return
    print(f"--- Search for '{query}' in {filename} ---")
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    matches = [m.start() for m in re.finditer(query, content)]
    for m in matches[:5]:
        start_idx = max(0, m - 100)
        end_idx = min(len(content), m + 150)
        print(content[start_idx:end_idx].replace('\n', ' '))

import re
search_in_file('test_script.jsx', 'paper-page')
search_in_file('Madhav_Drafting_Hub_dev.html', 'paper-page')
search_in_file('Madhav_Drafting_Hub_dev.html', '<style>')
