import re

def main():
    with open('Madhav_Drafting_Hub_Final_Registry.html', 'r', encoding='utf-8') as f:
        src = f.read()
    
    with open('Madhav_Drafting_Hub.html', 'r', encoding='utf-8') as f:
        dst = f.read()

    # 1. State
    state_match = re.search(r"(\s*// State for GNIDA Registry\s*const \[gnidaRegistryData, setGnidaRegistryData\].*?\}\);)", src, re.DOTALL)
    if state_match:
        state_code = state_match.group(1)
        # inject after defaultATSData declaration in dst
        dst = re.sub(r"(const defaultATSData = \{.*?\};\s*const \[atsData, setAtsData\] = useState\(defaultATSData\);)", r"\1\n" + state_code, dst, flags=re.DOTALL)
    
    # 2. Add Tab rendering button
    # Replace activeTab === 'COMING_SOON' with activeTab === 'GNIDA_REGISTRY'
    # Wait, the button might already be there in dst, let's find the second COMING_SOON
    # It's better to replace the Registry button explicitly.
    registry_button = r"""                                    <button
                                        onClick={() => setActiveTab('GNIDA_REGISTRY')}
                                        className={`flex-none px-4 py-2.5 text-sm font-bold rounded-xl transition-all border snap-start whitespace-nowrap flex items-center gap-2 ${activeTab === 'GNIDA_REGISTRY' ? 'bg-cyan-50 border-cyan-200 text-cyan-700 shadow-sm ring-1 ring-cyan-100' : 'bg-white border-gray-100 text-gray-500 hover:border-gray-200 hover:text-gray-700'}`}
                                    >
                                        <i className="fa-solid fa-book"></i> Registry
                                    </button>"""
                                    
    # Find the matching COMING_SOON registry button in dst and replace
    dst = re.sub(r"(\s*<button\s*onClick=\{\(\) => setActiveTab\('COMING_SOON'\)\}\s*className=\{`flex-none.*?\s*>\s*<i className=\"fa-solid fa-book\"></i> Registry\s*</button>)", registry_button, dst)

    # 3. Input UI
    input_match = re.search(r"(\s*\{activeTab === 'GNIDA_REGISTRY' && \(\s*<>\s*<Section title=\"Property Details.*?</>\s*\)\})", src, re.DOTALL)
    if input_match:
        input_code = input_match.group(1)
        # inject before {activeTab === 'REG_RENT' && ( in dst
        # wait, let's just insert it at the very bottom of the input forms, before the closing </div> of Scrollable Form Area.
        # Actually in dst, there is '{/* --- OTHER TABS --- */}' or something similar?
        dst = re.sub(r"(\s*\{/\* --- OTHER TABS --- \*/\})", r"\n" + input_code + r"\1", dst)
        if input_code not in dst: # fallback
             dst = re.sub(r"(\s*\{activeTab === 'REG_RENT' && \()", r"\n" + input_code + "\n" + r"\1", dst)

    # 4. Preview Document
    preview_match = re.search(r"(\s*\{activeTab === 'GNIDA_REGISTRY' && \(\s*<>\s*\{/\* PAGE 1: Data Sheet \*/\}.*?</>\s*\)\})", src, re.DOTALL)
    if preview_match:
        preview_code = preview_match.group(1)
        # inject before {activeTab === 'REG_RENT' && ( in document preview area.
        dst = re.sub(r"(\s*\{activeTab === 'REG_RENT' && \(\s*<div className=\"paper-page print-break)", r"\n" + preview_code + "\n" + r"\1", dst)

    # Write back
    with open('Madhav_Drafting_Hub_merged.html', 'w', encoding='utf-8') as f:
        f.write(dst)
    
    print("Merge script executed successfully. Check Madhav_Drafting_Hub_merged.html")

if __name__ == '__main__':
    main()
