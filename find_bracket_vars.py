with open('test_script.jsx', 'r', encoding='utf-8') as f:
    text = f.read()

import re
brackets = re.findall(r'\[[A-Za-z0-9_ ]+\]', text)
print("Bracket occurrences:", len(brackets))
if brackets:
    print("Sample bracket occurrences:", brackets[:10])
else:
    # Let's search for how input fields are rendered in the preview of another form like RENT or ATS
    print("No bracket matches found. Let's search for RENT or ATS preview spans.")
    matches = re.findall(r'className=["\'][^"\']*bg-yellow-50[^"\']*["\']', text)
    print("bg-yellow-50 matches:", len(matches))
