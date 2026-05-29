import re

with open('Madhav_Drafting_Hub.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Let's search for Advocate Madhav Maheshwari or similar
print("--- Searching for Madhav Maheshwari ---")
matches = list(re.finditer(r'(Madhav|Maheshwari)', content, re.IGNORECASE))
print(f"Total matches found: {len(matches)}")

for m in matches:
    # Print the line number and surrounding text
    start = max(0, m.start() - 50)
    end = min(len(content), m.end() + 100)
    line_num = content[:m.start()].count('\n') + 1
    snippet = content[start:end].replace('\n', ' ')
    print(f"Line {line_num}: {snippet}")
