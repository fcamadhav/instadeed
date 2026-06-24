import re

with open(r'C:\Users\fcama\.gemini\antigravity\scratch\madhav-legal-drafter\test_script.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

# ============================================================
# 1. UPDATE ALL PRICES
# ============================================================

price_map = {
    # templates array in renderHomeDashboard
    "price: '₹499'": "price: '₹300'",
    "price: '₹999'": "price: '₹300'",
    "price: '₹1,499'": "price: '₹5000'",
    "price: '₹299'": "price: '₹4000'",
    "price: '₹199'": "price: '₹0'",
    "price: '₹1,999'": "price: '₹10000'",
    "price: '₹399'": "price: '₹7500'",
    "price: '₹249'": "price: '₹500'",
    # Specific ones -- need to handle KYA specially
    # TM_APP was ₹499 -> ₹2000
    # NOIDA_TRANSFER was ₹499 -> ₹2000
    # GNIDA_PACKAGE was ₹1,999 -> ₹40000
    
    # Banner prices
    "price: '₹499', color: 'blue', icon: 'fa-file-signature', type: 'RENT'": "price: '₹300', color: 'blue', icon: 'fa-file-signature', type: 'RENT'",
    "price: '₹1,999', color: 'cyan', icon: 'fa-book', type: 'GNIDA_REGISTRY'": "price: '₹10000', color: 'cyan', icon: 'fa-book', type: 'GNIDA_REGISTRY'",
}

# Need to handle GNIDA_PACKAGE (₹1,999 -> ₹40000) and TM_APP (₹499 -> ₹2000), NOIDA_TRANSFER (₹499 -> ₹2000)
# But these appear in docMap objects where prices are next to labels
# Let me do targeted replacements for specific template lines

# The tricky part is that ₹499 appears for both RENT, TM_APP, and NOIDA_TRANSFER
# ₹1,999 appears for both GNIDA_REGISTRY and GNIDA_PACKAGE
# Let me use more context to distinguish

# In templates array:
content = content.replace(
    "price: '₹999'",
    "price: '₹300'"
)
content = content.replace(
    "price: '₹1,499'",
    "price: '₹5000'"
)
content = content.replace(
    "price: '₹1,999'",
    "price: '₹10000'"
)
content = content.replace(
    "price: '₹399'",
    "price: '₹7500'"
)
content = content.replace(
    "price: '₹249'",
    "price: '₹500'"
)

# Now handle the ambiguous ones with more context

# RENT price -> ₹300 (was ₹499)
content = content.replace(
    "label: 'Rent Agreement', desc: 'Standard residential rent agreement detailing landlord, tenant, security deposit, and tenancy clauses.', icon: 'fa-file-signature', color: 'blue', price: '₹300'",
    "label: 'Rent Agreement', desc: 'Standard residential rent agreement detailing landlord, tenant, security deposit, and tenancy clauses.', icon: 'fa-file-signature', color: 'blue', price: '₹300'"
)

# The GA actually already replaced ₹499 with ₹300 and ₹1,499 with ₹5,000 above.
# But wait - I replaced ₹1,499 so that's fine.

# Let me now handle GNIDA_PACKAGE ₹10000 -> ₹40000 (it was already changed from ₹1,999)
content = content.replace(
    "label: 'GNIDA Flat Registry Deed', desc: 'Sub-lease transfer deed format for residential flats under Greater Noida Authority.', icon: 'fa-book', color: 'cyan', price: '₹10000'",
    "label: 'GNIDA Flat Registry Deed', desc: 'Sub-lease transfer deed format for residential flats under Greater Noida Authority.', icon: 'fa-book', color: 'cyan', price: '₹10000'"
)

# Let me be more careful. Actually, the replacement of ₹1,999 -> ₹10000 happens everywhere,
# including GNIDA_PACKAGE which should be ₹40000. And the replacement of ₹499 -> ₹300 happens
# everywhere including TM_APP and NOIDA_TRANSFER which should be ₹2000.

# Let me re-do this more carefully. First revert, then do targeted replacements.

# Actually, let me just reload the file and do things differently.

with open(r'C:\Users\fcama\.gemini\antigravity\scratch\madhav-legal-drafter\test_script.jsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Do line-by-line targeted replacements
# We need to handle specific patterns in:
# 1. templates array (renderHomeDashboard)
# 2. banners array
# 3. docMap in flowStep 2
# 4. docMap in confirmDoc modal

result_lines = []
for line in lines:
    # Skip e-commerce form sections entirely (lines for ECOMM_TC, ECOMM_PP, ECOMM_RP)
    # We'll handle this below with a separate pass
    
    # Price updates with enough context to be unique
    
    # --- templates array (renderHomeDashboard) ---
    
    # RENT: ₹499 -> ₹300
    if "type: 'RENT', auth: 'ALL', cat: 'REAL_ESTATE', label: 'Rent Agreement'" in line and "price: '₹499'" in line:
        line = line.replace("price: '₹499'", "price: '₹300'")
    
    # ATS: ₹999 -> ₹300  
    elif "type: 'ATS', auth: 'ALL', cat: 'REAL_ESTATE', label: 'Agreement to Sell'" in line and "price: '₹999'" in line:
        line = line.replace("price: '₹999'", "price: '₹300'")
    
    # REG_RENT: ₹1,499 -> ₹5000
    elif "type: 'REG_RENT', auth: 'ALL', cat: 'REAL_ESTATE', label: 'Registered Rent Agreement'" in line and "price: '₹1,499'" in line:
        line = line.replace("price: '₹1,499'", "price: '₹5000'")
    
    # MUTATION: ₹299 -> ₹4000
    elif "type: 'MUTATION', auth: 'GNIDA', cat: 'AUTHORITY', label: 'Mutation Form'" in line and "price: '₹299'" in line:
        line = line.replace("price: '₹299'", "price: '₹4000'")
    
    # KYA (GNIDA): ₹199 -> ₹0 (FREE)
    elif "type: 'GNIDA', auth: 'GNIDA', cat: 'AUTHORITY', label: 'Know Your Allottee (KYA)'" in line and "price: '₹199'" in line:
        line = line.replace("price: '₹199'", "price: 'FREE'")
    
    # GNIDA_REGISTRY: ₹1,999 -> ₹10000
    elif "type: 'GNIDA_REGISTRY', auth: 'GNIDA', cat: 'AUTHORITY', label: 'GNIDA Flat Registry Deed'" in line and "price: '₹1,999'" in line:
        line = line.replace("price: '₹1,999'", "price: '₹10000'")
    
    # GNIDA_PTM: ₹399 -> ₹7500
    elif "type: 'GNIDA_PTM', auth: 'GNIDA', cat: 'AUTHORITY', label: 'Permission to Mortgage (PTM)'" in line and "price: '₹399'" in line:
        line = line.replace("price: '₹399'", "price: '₹7500'")
    
    # NOIDA_TRANSFER: ₹499 -> ₹2000
    elif "type: 'NOIDA_TRANSFER', auth: 'NOIDA', cat: 'AUTHORITY', label: 'Noida Transfer Application'" in line and "price: '₹499'" in line:
        line = line.replace("price: '₹499'", "price: '₹2000'")
    
    # TM48: ₹249 -> ₹500
    elif "type: 'TM48', auth: 'ALL', cat: 'TRADE', label: 'TM-48 Trademark Proxy'" in line and "price: '₹249'" in line:
        line = line.replace("price: '₹249'", "price: '₹500'")
    
    # --- Banners array ---
    # RENT banner
    elif "title: 'Rent Agreement', subtitle: 'Most Popular" in line and "price: '₹499'" in line:
        line = line.replace("price: '₹499'", "price: '₹300'")
    
    # GNIDA_REGISTRY banner
    elif "title: 'GNIDA Registry Deed', subtitle: 'Flat sub-lease transfer format'" in line and "price: '₹1,999'" in line:
        line = line.replace("price: '₹1,999'", "price: '₹10000'")
    
    # --- docMap in flowStep 2 (confirmDoc details page) ---
    
    # RENT docMap
    elif "RENT: { label: 'Rent Agreement', icon: 'fa-file-signature', desc: 'Standard residential rent agreement" in line and "price: '₹499'" in line:
        line = line.replace("price: '₹499'", "price: '₹300'")
    
    # ATS docMap
    elif "ATS: { label: 'Agreement to Sell', icon: 'fa-file-contract', desc: 'Legal contract for sale/purchase" in line and "price: '₹999'" in line:
        line = line.replace("price: '₹999'", "price: '₹300'")
    
    # REG_RENT docMap
    elif "REG_RENT: { label: 'Registered Rent Agreement', icon: 'fa-stamp', desc: 'Official format registered lease" in line and "price: '₹1,499'" in line:
        line = line.replace("price: '₹1,499'", "price: '₹5000'")
    
    # TM48 docMap
    elif "TM48: { label: 'TM-48 Trademark Proxy', icon: 'fa-trademark', desc: 'Official authorisation form" in line and "price: '₹249'" in line:
        line = line.replace("price: '₹249'", "price: '₹500'")
    
    # GNIDA_PACKAGE docMap -> ₹40000
    elif "GNIDA_PACKAGE: { label: 'GNIDA 5-in-1 Package', icon: 'fa-cubes'" in line and "price: '₹1,999'" in line:
        line = line.replace("price: '₹1,999'", "price: '₹40000'")
    
    # KYA docMap
    elif "KYA: { label: 'Know Your Allottee (KYA)', icon: 'fa-id-card'" in line and "price: '₹199'" in line:
        line = line.replace("price: '₹199'", "price: 'FREE'")
    
    # TM_APP docMap -> ₹2000
    elif "TM_APP: { label: 'Transfer Memo Application', icon: 'fa-right-left'" in line and "price: '₹499'" in line:
        line = line.replace("price: '₹499'", "price: '₹2000'")
    
    # MUTATION docMap
    elif "MUTATION: { label: 'Mutation Form', icon: 'fa-file-pen'" in line and "price: '₹299'" in line:
        line = line.replace("price: '₹299'", "price: '₹4000'")
    
    # GNIDA_REGISTRY docMap
    elif "GNIDA_REGISTRY: { label: 'GNIDA Registry Format', icon: 'fa-book'" in line and "price: '₹1,999'" in line:
        line = line.replace("price: '₹1,999'", "price: '₹10000'")
    
    # GNIDA_PTM docMap
    elif "GNIDA_PTM: { label: 'Permission to Mortgage (PTM)', icon: 'fa-file-shield'" in line and "price: '₹399'" in line:
        line = line.replace("price: '₹399'", "price: '₹7500'")
    
    # NOIDA_TRANSFER docMap -> ₹2000
    elif "NOIDA_TRANSFER: { label: 'NOIDA Transfer Application', icon: 'fa-right-left'" in line and "price: '₹499'" in line:
        line = line.replace("price: '₹499'", "price: '₹2000'")
    
    # --- Second docMap (confirmDoc modal) ---
    
    # RENT confirm doc
    elif "RENT: { label: 'Rent Agreement', icon: 'fa-file-signature', color: 'blue'" in line and "price: '₹499'" in line:
        line = line.replace("price: '₹499'", "price: '₹300'")
    
    # ATS confirm doc
    elif "ATS: { label: 'Agreement to Sell', icon: 'fa-file-contract', color: 'purple'" in line and "price: '₹999'" in line:
        line = line.replace("price: '₹999'", "price: '₹300'")
    
    # REG_RENT confirm doc
    elif "REG_RENT: { label: 'Registered Rent Agreement', icon: 'fa-stamp', color: 'indigo'" in line and "price: '₹1,499'" in line:
        line = line.replace("price: '₹1,499'", "price: '₹5000'")
    
    # TM48 confirm doc
    elif "TM48: { label: 'TM-48 Trademark Proxy', icon: 'fa-trademark', color: 'orange'" in line and "price: '₹249'" in line:
        line = line.replace("price: '₹249'", "price: '₹500'")
    
    # GNIDA_PACKAGE confirm doc -> ₹40000
    elif "GNIDA_PACKAGE: { label: 'GNIDA 5-in-1 Package', icon: 'fa-cubes', color: 'blue'" in line and "price: '₹1,999'" in line:
        line = line.replace("price: '₹1,999'", "price: '₹40000'")
    
    # KYA confirm doc
    elif "KYA: { label: 'Know Your Allottee', icon: 'fa-id-card', color: 'yellow'" in line and "price: '₹199'" in line:
        line = line.replace("price: '₹199'", "price: 'FREE'")
    
    # TM_APP confirm doc -> ₹2000
    elif "TM_APP: { label: 'Transfer Memo Application', icon: 'fa-right-left', color: 'rose'" in line and "price: '₹499'" in line:
        line = line.replace("price: '₹499'", "price: '₹2000'")
    
    # MUTATION confirm doc
    elif "MUTATION: { label: 'Mutation Form', icon: 'fa-file-pen', color: 'indigo'" in line and "price: '₹299'" in line:
        line = line.replace("price: '₹299'", "price: '₹4000'")
    
    # GNIDA_REGISTRY confirm doc
    elif "GNIDA_REGISTRY: { label: 'GNIDA Registry Format', icon: 'fa-book', color: 'cyan'" in line and "price: '₹1,999'" in line:
        line = line.replace("price: '₹1,999'", "price: '₹10000'")
    
    # GNIDA_PTM confirm doc
    elif "GNIDA_PTM: { label: 'Permission to Mortgage (PTM)', icon: 'fa-file-shield', color: 'teal'" in line and "price: '₹399'" in line:
        line = line.replace("price: '₹399'", "price: '₹7500'")
    
    # NOIDA_TRANSFER confirm doc -> ₹2000
    elif "NOIDA_TRANSFER: { label: 'NOIDA Transfer Application', icon: 'fa-right-left', color: 'sky'" in line and "price: '₹499'" in line:
        line = line.replace("price: '₹499'", "price: '₹2000'")
    
    result_lines.append(line)

content = ''.join(result_lines)

# ============================================================
# 2. REMOVE ALL E-COMMERCE DOCUMENTS
# ============================================================

# Remove from templates array - the 3 e-commerce lines
# Pattern: lines containing ECOMM_TC, ECOMM_PP, ECOMM_RP in the templates array
import re

# Remove individual e-commerce template lines
# These are in the templates array: lines 3487-3489
content = re.sub(
    r'\s*\{ type: \'ECOMM_TC\'.*?\},\n',
    '\n',
    content
)
content = re.sub(
    r'\s*\{ type: \'ECOMM_PP\'.*?\},\n',
    '\n',
    content
)
content = re.sub(
    r'\s*\{ type: \'ECOMM_RP\'.*?\},\n',
    '\n',
    content
)

# Remove E-Commerce Bundle banner
content = re.sub(
    r'\s*\{ title: \'E-Commerce Bundle\'.*?\},\n',
    '\n',
    content
)

# Adjust bannerIdx rotation
content = content.replace(
    'const iv = setInterval(() => setBannerIdx(i => (i + 1) % 3), 4000);',
    'const iv = setInterval(() => setBannerIdx(i => (i + 1) % 2), 4000);'
)

# Remove E-Commerce from category filter pills
content = content.replace(
    ",\n                                { key: 'ECOMMERCE', label: 'E-Commerce', icon: 'fa-cart-shopping' }",
    ""
)
# Remove the trailing comma before this entry
content = content.replace(
    "{ key: 'AUTHORITY', label: 'Authority Forms', icon: 'fa-building-columns' },\n                                { key: 'TRADE', label: 'Business & Trade', icon: 'fa-briefcase' }",
    "{ key: 'AUTHORITY', label: 'Authority Forms', icon: 'fa-building-columns' },\n                                { key: 'TRADE', label: 'Business & Trade', icon: 'fa-briefcase' }"
)
content = content.replace(
    "{ key: 'AUTHORITY', label: 'Authority Forms', icon: 'fa-building-columns' },\n                                { key: 'ECOMMERCE', label: 'E-Commerce', icon: 'fa-cart-shopping' }",
    "{ key: 'AUTHORITY', label: 'Authority Forms', icon: 'fa-building-columns' }"
)

# Remove e-commerce entries from shareDocTypes
content = content.replace(
    ",\n                { value: 'ecomm_tc', label: 'E-Commerce T&C' },\n                { value: 'ecomm_pp', label: 'Privacy Policy' },\n                { value: 'ecomm_rp', label: 'Refund Policy' }",
    ""
)

# Remove e-commerce entries from ShareModal dropdown options
content = content.replace(
    "<option value=\"ecomm_tc\">E-Commerce T&amp;C</option>",
    ""
)
content = content.replace(
    "<option value=\"ecomm_pp\">Privacy Policy</option>",
    ""
)
content = content.replace(
    "<option value=\"ecomm_rp\">Refund Policy</option>",
    ""
)

# Remove from getEsignDetails map
content = content.replace(
    ",\n                    'ECOMM_TC': 'website-tos',\n                    'ECOMM_PP': 'e-commerce-privacy',\n                    'ECOMM_RP': 'ecomm_rp'",
    ""
)

# Remove from getEsignDetails URL matching
content = re.sub(
    r'\s*else if \(tabName === \'ECOMM_TC\' \&\& \(docLower\.includes\(\'e-commerce terms\'\) \|\| docLower\.includes\(\'ecomm_tc\'\) \|\| docLower\.includes\(\'website-tos\'\)\)\) isMatch = true;',
    '',
    content
)
content = re.sub(
    r'\s*else if \(tabName === \'ECOMM_PP\' \&\& \(docLower\.includes\(\'e-commerce privacy\'\) \|\| docLower\.includes\(\'ecomm_pp\'\) \|\| docLower\.includes\(\'privacy\'\)\)\) isMatch = true;',
    '',
    content
)
content = re.sub(
    r'\s*else if \(tabName === \'ECOMM_RP\' \&\& \(docLower\.includes\(\'refund\'\) \|\| docLower\.includes\(\'ecomm_rp\'\) \|\| docLower\.includes\(\'cancellation\'\)\)\) isMatch = true;',
    '',
    content
)

# Remove from URL param routing (docLower detection)
content = re.sub(
    r'\s*} else if \(docLower\.includes\(\'e-commerce terms\'\) \|\| docLower\.includes\(\'ecomm_tc\'\) \|\| docLower\.includes\(\'website-tos\'\)\) {\n\s+routedTab = \'ECOMM_TC\';\n\s+routedAuth = routedAuth \|\| \'ECOMMERCE\';',
    '',
    content
)
content = re.sub(
    r'\s*} else if \(docLower\.includes\(\'e-commerce privacy\'\) \|\| docLower\.includes\(\'ecomm_pp\'\) \|\| docLower\.includes\(\'privacy\'\)\) {\n\s+routedTab = \'ECOMM_PP\';\n\s+routedAuth = routedAuth \|\| \'ECOMMERCE\';',
    '',
    content
)
content = re.sub(
    r'\s*} else if \(docLower\.includes\(\'refund\'\) \|\| docLower\.includes\(\'ecomm_rp\'\) \|\| docLower\.includes\(\'cancellation\'\) \|\| docLower\.includes\(\'cancellation policy\'\)\) {\n\s+routedTab = \'ECOMM_RP\';\n\s+routedAuth = routedAuth \|\| \'ECOMMERCE\';',
    '',
    content
)

# Remove the ECOMMERCE authority section from sidebar doc grid (lines 5249-5303)
content = re.sub(
    r'\n\s+{\s+\(activeAuthority === \'ECOMMERCE\'\) && \([\s\S]*?\)\s+}',
    '',
    content
)

# Remove e-commerce section from sidebar editing labels
content = content.replace(
    "activeTab === 'ECOMM_TC' ? 'Terms & Conditions' :\n                                                activeTab === 'ECOMM_PP' ? 'Privacy Policy' :\n                                                activeTab === 'ECOMM_RP' ? 'Refund Policy' :",
    ""
)
# Also remove the colon at end of previous line (clean up)
# Actually this might leave a dangling colon - let me check and fix
# The pattern is: `activeTab === 'GNIDA_PTM' ? 'Permission to Mortgage' :`
# followed by the ECOMM lines then a colon. Let me clean up properly.

# Remove state declarations for ecommerce data
content = re.sub(
    r'\s+const defaultEcommTCData = \{[^}]*\};',
    '',
    content
)
content = re.sub(
    r'\s+const defaultEcommPPData = \{[^}]*\};',
    '',
    content
)
content = re.sub(
    r'\s+const defaultEcommRPData = \{[^}]*\};',
    '',
    content
)
content = re.sub(
    r'\s+const \[ecommTCData, setEcommTCData\] = useState\(defaultEcommTCData\);',
    '',
    content
)
content = re.sub(
    r'\s+const \[ecommPPData, setEcommPPData\] = useState\(defaultEcommPPData\);',
    '',
    content
)
content = re.sub(
    r'\s+const \[ecommRPData, setEcommRPData\] = useState\(defaultEcommRPData\);',
    '',
    content
)

# Remove e-commerce from cloud view loading
content = re.sub(
    r'\s+else if \(tPayload\.type === \'ECOMM_TC\'\) setEcommTCData\(tPayload\.payload\);',
    '',
    content
)
content = re.sub(
    r'\s+else if \(tPayload\.type === \'ECOMM_PP\'\) setEcommPPData\(tPayload\.payload\);',
    '',
    content
)
content = re.sub(
    r'\s+else if \(tPayload\.type === \'ECOMM_RP\'\) setEcommRPData\(tPayload\.payload\);',
    '',
    content
)

# Remove from localstorage loading
content = re.sub(
    r'\s+if \(parsed\.ecommTC\) setEcommTCData\(prev => \({ \.\.\.prev, \.\.\.parsed\.ecommTC }\);',
    '',
    content
)
content = re.sub(
    r'\s+if \(parsed\.ecommPP\) setEcommPPData\(prev => \({ \.\.\.prev, \.\.\.parsed\.ecommPP }\);',
    '',
    content
)
content = re.sub(
    r'\s+if \(parsed\.ecommRP\) setEcommRPData\(prev => \({ \.\.\.prev, \.\.\.parsed\.ecommRP }\);',
    '',
    content
)

# Remove from save data object
content = content.replace(
    ",\n                        ecommTC: ecommTCData,\n                        ecommPP: ecommPPData,\n                        ecommRP: ecommRPData",
    ""
)

# Remove from useEffect dependency array
content = content.replace(
    ", ecommTCData, ecommPPData, ecommRPData",
    ""
)

# Remove from downloadJSON
content = re.sub(
    r'\s+else if \(activeTab === \'ECOMM_TC\'\) { currentData = ecommTCData; name = ecommTCData\.companyName \|\| \'Draft\'; }',
    '',
    content
)
content = re.sub(
    r'\s+else if \(activeTab === \'ECOMM_PP\'\) { currentData = ecommPPData; name = ecommPPData\.companyName \|\| \'Draft\'; }',
    '',
    content
)
content = re.sub(
    r'\s+else if \(activeTab === \'ECOMM_RP\'\) { currentData = ecommRPData; name = ecommRPData\.companyName \|\| \'Draft\'; }',
    '',
    content
)

# Remove from uploadJSON
content = re.sub(
    r'\s+else if \(activeTab === \'ECOMM_TC\'\) setEcommTCData\(prev => \({ \.\.\.prev, \.\.\.loaded }\);',
    '',
    content
)
content = re.sub(
    r'\s+else if \(activeTab === \'ECOMM_PP\'\) setEcommPPData\(prev => \({ \.\.\.prev, \.\.\.loaded }\);',
    '',
    content
)
content = re.sub(
    r'\s+else if \(activeTab === \'ECOMM_RP\'\) setEcommRPData\(prev => \({ \.\.\.prev, \.\.\.loaded }\);',
    '',
    content
)

# Remove from clearAllData
content = re.sub(
    r'\s+setEcommTCData\(defaultEcommTCData\);',
    '',
    content
)
content = re.sub(
    r'\s+setEcommPPData\(defaultEcommPPData\);',
    '',
    content
)
content = re.sub(
    r'\s+setEcommRPData\(defaultEcommRPData\);',
    '',
    content
)

# Remove from saveDefault
content = re.sub(
    r'\s+else if \(activeTab === \'ECOMM_TC\'\) currentData = ecommTCData;',
    '',
    content
)
content = re.sub(
    r'\s+else if \(activeTab === \'ECOMM_PP\'\) currentData = ecommPPData;',
    '',
    content
)
content = re.sub(
    r'\s+else if \(activeTab === \'ECOMM_RP\'\) currentData = ecommRPData;',
    '',
    content
)

# Remove from buildDocumentName (title)
content = re.sub(
    r'\s+else if \(activeTab === \'ECOMM_TC\'\) name = buildDocumentName\(\'\', ecommTCData\.companyName, \'E-Commerce T&C\'\);',
    '',
    content
)
content = re.sub(
    r'\s+else if \(activeTab === \'ECOMM_PP\'\) name = buildDocumentName\(\'\', ecommPPData\.companyName, \'E-Commerce Privacy\'\);',
    '',
    content
)
content = re.sub(
    r'\s+else if \(activeTab === \'ECOMM_RP\'\) name = buildDocumentName\(\'\', ecommRPData\.companyName, \'Refund Policy\'\);',
    '',
    content
)

# Remove from saveToLibrary
content = re.sub(
    r'\s+else if \(activeTab === \'ECOMM_TC\'\) { currentData = ecommTCData; defaultName = buildDocumentName\(\'\', ecommTCData\.companyName, "E-Commerce T&C"\); }',
    '',
    content
)
content = re.sub(
    r'\s+else if \(activeTab === \'ECOMM_PP\'\) { currentData = ecommPPData; defaultName = buildDocumentName\(\'\', ecommPPData\.companyName, "E-Commerce Privacy"\); }',
    '',
    content
)
content = re.sub(
    r'\s+else if \(activeTab === \'ECOMM_RP\'\) { currentData = ecommRPData; defaultName = buildDocumentName\(\'\', ecommRPData\.companyName, "Refund Policy"\); }',
    '',
    content
)

# Remove from loadFromLibrary
content = re.sub(
    r'\s+else if \(draft\.type === \'ECOMM_TC\'\) setEcommTCData\(draft\.data\);',
    '',
    content
)
content = re.sub(
    r'\s+else if \(draft\.type === \'ECOMM_PP\'\) setEcommPPData\(draft\.data\);',
    '',
    content
)
content = re.sub(
    r'\s+else if \(draft\.type === \'ECOMM_RP\'\) setEcommRPData\(draft\.data\);',
    '',
    content
)

# Remove from loadDefault
content = re.sub(
    r'\s+else if \(activeTab === \'ECOMM_TC\'\) setEcommTCData\(parsed\);',
    '',
    content
)
content = re.sub(
    r'\s+else if \(activeTab === \'ECOMM_PP\'\) setEcommPPData\(parsed\);',
    '',
    content
)
content = re.sub(
    r'\s+else if \(activeTab === \'ECOMM_RP\'\) setEcommRPData\(parsed\);',
    '',
    content
)

# Remove handleChange for e-commerce tabs
content = re.sub(
    r'\s+if \(activeTab === \'ECOMM_TC\'\) \{\s+setEcommTCData\(prev => \({ \.\.\.prev, \[name\]: value }\);\s+return;\s+}',
    '',
    content
)
content = re.sub(
    r'\s+if \(activeTab === \'ECOMM_PP\'\) \{\s+setEcommPPData\(prev => \({ \.\.\.prev, \[name\]: value }\);\s+return;\s+}',
    '',
    content
)
content = re.sub(
    r'\s+if \(activeTab === \'ECOMM_RP\'\) \{\s+setEcommRPData\(prev => \({ \.\.\.prev, \[name\]: value }\);\s+return;\s+}',
    '',
    content
)

# Remove from getActiveDataPayload
content = re.sub(
    r'\s+else if \(activeTab === \'ECOMM_TC\'\) payload = ecommTCData;',
    '',
    content
)
content = re.sub(
    r'\s+else if \(activeTab === \'ECOMM_PP\'\) payload = ecommPPData;',
    '',
    content
)
content = re.sub(
    r'\s+else if \(activeTab === \'ECOMM_RP\'\) payload = ecommRPData;',
    '',
    content
)

# Remove from extractCustomerDetails
content = re.sub(
    r'\s+} else if \(activeTab === \'ECOMM_TC\' \|\| activeTab === \'ECOMM_PP\' \|\| activeTab === \'ECOMM_RP\'\) {\n\s+name = ecommTCData\.companyName \|\| \'\';',
    '',
    content
)

# Remove from CRM order loading (Load button in CRM)
content = re.sub(
    r'\s+else if \(tPayload\.type === \'ECOMM_TC\'\) setEcommTCData\(tPayload\.payload\);',
    '',
    content
)
content = re.sub(
    r'\s+else if \(tPayload\.type === \'ECOMM_PP\'\) setEcommPPData\(tPayload\.payload\);',
    '',
    content
)
content = re.sub(
    r'\s+else if \(tPayload\.type === \'ECOMM_RP\'\) setEcommRPData\(tPayload\.payload\);',
    '',
    content
)

# Remove the ECOMMERCE routing in docParam section
content = re.sub(
    r'\s+else if \(docLower\.includes\(\'e-commerce terms\'\) \|\| docLower\.includes\(\'ecomm_tc\'\) \|\| docLower\.includes\(\'website-tos\'\)\) {\n\s+routedTab = \'ECOMM_TC\';\n\s+routedAuth = \'ECOMMERCE\';',
    '',
    content
)

# Remove e-commerce form sections (large blocks)
# ECOMM_TC form section
content = re.sub(
    r'\n\s+{\(activeTab === \'ECOMM_TC\'\) && \(\n\s+<>\n\s+<Section title="Company Information".*?<\/>\n\s+\)}',
    '',
    content,
    flags=re.DOTALL
)

# ECOMM_PP form section
content = re.sub(
    r'\n\s+{\(activeTab === \'ECOMM_PP\'\) && \(\n\s+<>\n\s+<Section title="Company Information".*?<\/>\n\s+\)}',
    '',
    content,
    flags=re.DOTALL
)

# ECOMM_RP form section
content = re.sub(
    r'\n\s+{\(activeTab === \'ECOMM_RP\'\) && \(\n\s+<>\n\s+<Section title="Company Information".*?<\/>\n\s+\)}',
    '',
    content,
    flags=re.DOTALL
)

# Sort of a hack - remove the comment about ecommerce
content = content.replace(
    "            // --- E-COMMERCE DOCUMENT STATES ---",
    ""
)

# Remove the "E-Commerce" from sidebar (the activeAuthority === 'ECOMMERCE' section)
# This was already handled above

# Fix the docMap in flowStep 2 to remove e-commerce entries
content = re.sub(
    r',\n\s+ECOMM_TC: \{ label: \'Website Terms of Service\'.*?\},\n\s+ECOMM_PP: \{ label: \'Website Privacy Policy\'.*?\},\n\s+ECOMM_RP: \{ label: \'Refund & Return Policy\'.*?\}',
    '',
    content
)

# Fix the confirmDoc docMap to remove e-commerce entries
content = re.sub(
    r',\n\s+ECOMM_TC: \{ label: \'Website Terms of Service\'.*?\},\n\s+ECOMM_PP: \{ label: \'Website Privacy Policy\'.*?\},\n\s+ECOMM_RP: \{ label: \'Refund & Return Policy\'.*?\}',
    '',
    content
)

# Clean up: Fix the editing label for GNIDA_PTM (remove trailing colon when e-com lines are removed)
# This is tricky - need to find the exact pattern
content = content.replace(
    "activeTab === 'GNIDA_PTM' ? 'Permission to Mortgage' :\n                                                activeTab === 'ECOMM_TC' ? 'Terms & Conditions' :\n                                                activeTab === 'ECOMM_PP' ? 'Privacy Policy' :\n                                                activeTab === 'ECOMM_RP' ? 'Refund Policy' :\n                                                activeTab === 'NOIDA_TRANSFER' ? 'Noida Transfer' :",
    "activeTab === 'GNIDA_PTM' ? 'Permission to Mortgage' :\n                                                activeTab === 'NOIDA_TRANSFER' ? 'Noida Transfer' :"
)

# Clean up: Fix editing label for TM_APP since GNIDA_PTM follows it
# Actually let me check if the lines after removal still make sense
content = content.replace(
    "activeTab === 'TM_APP' ? 'Transfer Memo' :\n                                                activeTab === 'MUTATION' ? 'Mutation Form' :\n                                                activeTab === 'GNIDA_REGISTRY' ? 'Registry Format' :",
    "activeTab === 'TM_APP' ? 'Transfer Memo' :\n                                                activeTab === 'MUTATION' ? 'Mutation Form' :\n                                                activeTab === 'GNIDA_REGISTRY' ? 'Registry Format' :"
)

# Clean up: Ensure line continuity after all deletions
# Remove any truly empty lines left by multiple deletions (more than 2 consecutive empty lines)
content = re.sub(r'\n{4,}', '\n\n\n', content)

with open(r'C:\Users\fcama\.gemini\antigravity\scratch\madhav-legal-drafter\test_script.jsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("Script completed successfully")
print(f"Total characters written: {len(content)}")
