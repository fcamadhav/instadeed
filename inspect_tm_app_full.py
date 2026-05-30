with open('test_script.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

pos = content.find("activeTab === 'TM_APP'")
if pos == -1:
    print("TM_APP tab not found")
    exit()

# Print the next 3000 chars of TM_APP block
print("=== TM_APP Start ===")
print(content[pos:pos+3000])

print("\n--- Search for PAGE comments inside TM_APP tab ---")
import re
# Look for PAGE comments within the next 120000 characters
subcontent = content[pos:pos+120000]
page_matches = re.finditer(r'\{\s*/\*\s*(PAGE\s+\d+:[^*]*)\s*\*/\s*\}', subcontent)
for pm in page_matches:
    idx = pos + pm.start()
    comment = pm.group(1).strip()
    # Also find next footer in page
    end_idx = subcontent.find("PAGE", pm.end())
    if end_idx == -1:
        end_idx = len(subcontent)
    page_block = subcontent[pm.end():end_idx]
    footer_match = re.search(r'Page\s+(\d+)', page_block)
    footer_num = footer_match.group(1) if footer_match else "Not found"
    
    print(f"Index {idx}: Comment='{comment}', Footer Page={footer_num}")
