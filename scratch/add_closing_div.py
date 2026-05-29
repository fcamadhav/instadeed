file_path = 'Madhav_Drafting_Hub.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Locate the block:
#                             </div>
#                         )}
# 
#                         {/* Gated Authentication Overlay */}
# We want to replace it with:
#                             </div>
#                         )}
#                     </div>
# 
#                         {/* Gated Authentication Overlay */}

target = '                            </div>\n                        )}\n\n                        {/* Gated Authentication Overlay */}'
replacement = '                            </div>\n                        )}\n                    </div>\n\n                        {/* Gated Authentication Overlay */}'

if target in content:
    content = content.replace(target, replacement)
    print("Found and replaced target with carriage-return handling check...")
else:
    # Try with \r\n (Windows line endings)
    target_rn = '                            </div>\r\n                        )}\r\n\r\n                        {/* Gated Authentication Overlay */}'
    replacement_rn = '                            </div>\r\n                        )}\r\n                    </div>\r\n\r\n                        {/* Gated Authentication Overlay */}'
    if target_rn in content:
        content = content.replace(target_rn, replacement_rn)
        print("Found and replaced target with Windows line endings.")
    else:
        # Fallback to a regex
        import re
        pattern = r'(</div>\s*\)\s*}\s*\n)(\s*/\* Gated Authentication Overlay \*/)'
        match = re.search(pattern, content)
        if match:
            print("Found via regex match.")
            matched_text = match.group(0)
            replacement_text = match.group(1) + '                    </div>\n\n' + match.group(2)
            content = content.replace(matched_text, replacement_text)
        else:
            print("Target block not found.")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Finished add_closing_div execution.")
