with open('test_script.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

import re

# Find activeTab state setup or sidebar tabs
# E.g. setActiveTab('...') or activeTab === '...'
tabs = re.findall(r"activeTab === '([^']+)'", content)
print("Unique activeTab keys used in conditional renders:", list(set(tabs)))
