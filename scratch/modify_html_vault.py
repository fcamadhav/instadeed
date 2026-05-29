import re

file_path = 'Madhav_Drafting_Hub.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

def safe_replace(text, target, rep):
    if target in text:
        return text.replace(target, rep)
    target_rn = target.replace('\n', '\r\n')
    rep_rn = rep.replace('\n', '\r\n')
    if target_rn in text:
        return text.replace(target_rn, rep_rn)
    print(f"FAILED TO REPLACE BLOCK: {repr(target[:80])}...")
    return text

# 6. Close Left Sidebar wrapper safely (idempotent check)
if 'Sign Out from Admin CRM\n                                    </button>\n                                </div>\n                            )}\n                        </div >\n                    )}' not in content:
    target_close_sidebar = """                    </div >

                    {/* Right Preview Area */}"""
    
    rep_close_sidebar = """                    </div >
                    )}

                    {/* Right Preview Area */}"""
    content = safe_replace(content, target_close_sidebar, rep_close_sidebar)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Indentation fix applied!")
