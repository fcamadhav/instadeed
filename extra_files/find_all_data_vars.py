import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('test_script.jsx', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Find all words that end in "Data" or contain "Data"
words = re.findall(r'\b[a-zA-Z0-9_]*Data\b', content)
unique_words = sorted(list(set(words)))

print("Found unique words ending/containing 'Data':")
for w in unique_words:
    print("  ", w)
