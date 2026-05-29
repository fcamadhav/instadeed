import re

with open('Madhav_Drafting_Hub.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Remove state
text = re.sub(r'(\s*// State for GNIDA Registry.*?\}\);)', '', text, flags=re.DOTALL)

# Remove input section EXACTLY as it was inserted
text = re.sub(r'(\s*\{activeTab === \'GNIDA_REGISTRY\' && \(\s*<>\s*<Section title=\"Property Details.*?</button>\s*</Section>\s*<Section title=\"Dates\" icon=\"fa-calendar-check\" color=\"cyan\">)', '', text, flags=re.DOTALL)

# Remove preview section EXACTLY as it was inserted
text = re.sub(r'(\s*\{activeTab === \'GNIDA_REGISTRY\' && \(\s*<>\s*\{\/\* PAGE 1: Data Sheet \*\/\}.*?</>\s*\)\})', '', text, flags=re.DOTALL)

with open('Madhav_Drafting_Hub.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Reverted!")
