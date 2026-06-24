import re

with open('Madhav_Drafting_Hub_Final_Registry.html', 'r', encoding='utf-8') as f:
    src_lines = f.readlines()
preview_code = "".join(src_lines[3577:3801])

with open('Madhav_Drafting_Hub.html', 'r', encoding='utf-8') as f:
    d_lines = f.readlines()

for i, line in enumerate(d_lines):
    # This is the Preview Section injection
    if "{activeTab === 'GNIDA_PTM' && (" in line and "paper-page" in d_lines[i+1] and "MORTGAGE" in d_lines[i+5]:
        d_lines.insert(i, preview_code + "\n")
        break

with open('Madhav_Drafting_Hub.html', 'w', encoding='utf-8') as f:
    f.writelines(d_lines)

print("Injected Preview Code!")
