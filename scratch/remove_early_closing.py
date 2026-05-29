import re

file_path = 'Madhav_Drafting_Hub.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# We want to replace:
#                                     }
# 
#                                  </div >
#                          </div >
# 
#                          {/* Library Modal

# Let's use a regex to match this block, taking care of spaces and newlines
pattern = r'activeTab === \'COMING_SOON\'\s*&&\s*\(\s*<div className="paper-page text-center p-20 flex flex-col items-center justify-center text-gray-400 mt-8 bg-white shadow-lg rounded-xl border border-gray-100">.*?</div>\s*\)\s*}\s*\n\s*</div\s*>\s*\n\s*</div\s*>'
match = re.search(pattern, content, re.DOTALL)
if match:
    print("Found match!")
    # We want to replace the trailing closing divs with nothing, i.e., keep only up to the closing brace }
    matched_text = match.group(0)
    # Re-construct without the trailing </div > </div >
    replacement = matched_text.split('}')[0] + '}' + '\n'
    new_content = content.replace(matched_text, replacement)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Successfully removed early closing tags.")
else:
    print("Pattern not found. Trying secondary match...")
    # Let's try matching the exact lines around 7380-7386
    sub_pattern = r'(\s*\)\s*}\s*\n)(\s*</div\s*>\s*\n\s*</div\s*>\s*\n)'
    # Let's inspect around COMING_SOON
    idx = content.find('activeTab === \'COMING_SOON\'')
    if idx != -1:
        print("Found COMING_SOON tab reference in HTML.")
        # Find the next occurrences of </div >
        sub_content = content[idx:idx+2000]
        match_sub = re.search(r'}\s*\n\s*</div\s*>\s*\n\s*</div\s*>\s*\n', sub_content)
        if match_sub:
            print("Found closing tags in sub_content.")
            target_str = match_sub.group(0)
            replacement_str = '}\n'
            new_sub_content = sub_content.replace(target_str, replacement_str)
            new_content = content[:idx] + content[idx:].replace(sub_content, new_sub_content, 1)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print("Successfully removed early closing tags via sub-content match.")
        else:
            print("Could not find closing tags near COMING_SOON.")
    else:
        print("COMING_SOON not found.")
