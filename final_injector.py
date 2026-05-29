import re

def main():
    with open('Madhav_Drafting_Hub_Final_Registry.html', 'r', encoding='utf-8') as f:
        src_lines = f.readlines()
    
    with open('Madhav_Drafting_Hub.html', 'r', encoding='utf-8') as f:
        dest = f.read()

    # 1. State extraction
    state_code = "".join(src_lines[685:738])

    # 2. Input UI extraction (1151 to 1275)
    input_code = "".join(src_lines[1150:1275])

    # 3. Document Preview extraction (3578 to 3801)
    preview_code = "".join(src_lines[3577:3801])


    # INJECTION
    dest = dest.replace("const defaultATSData =", state_code + "\n            const defaultATSData =")

    # To be extremely safe, we inject input block exactly before `{activeTab === 'GNIDA_PTM' && (` in the inputs area
    with open('Madhav_Drafting_Hub.html', 'r', encoding='utf-8') as f:
        d_lines = f.readlines()
        
    for i, line in enumerate(d_lines):
        if "const defaultATSData = {" in line:
            d_lines.insert(i, state_code + "\n")
            break
            
    for i, line in enumerate(d_lines):
        if "{activeTab === 'GNIDA_PTM' && (" in line and "Section title=\"Application Details\"" in d_lines[i+2]:
            d_lines.insert(i, input_code + "\n")
            break

    for i, line in enumerate(d_lines):
        if "{activeTab === 'GNIDA_PTM' && (" in line and "paper-page" in d_lines[i+1] and "MORTGAGE" in d_lines[i+4]:
            d_lines.insert(i, preview_code + "\n")
            break

    out_text = "".join(d_lines)
    
    # 4. HandleChange
    handle_change_block = """
                if (activeTab === 'GNIDA_REGISTRY') {
                    setGnidaRegistryData(prev => ({ ...prev, [name]: value }));
                    return;
                }
"""
    out_text = out_text.replace("if (activeTab === 'GNIDA_PTM') {", handle_change_block + "                if (activeTab === 'GNIDA_PTM') {")

    # 5. Buttons & JSON Handlers
    button_pattern = r"""onClick=\{\(\) => setActiveTab\('COMING_SOON'\)\}\s*className=\{`flex-none px-4 py-2.5 text-sm font-bold rounded-xl transition-all border snap-start whitespace-nowrap flex items-center gap-2 \$\{activeTab === 'COMING_SOON' \? 'bg-cyan-50 border-cyan-200 text-cyan-700 shadow-sm ring-1 ring-cyan-100' : 'bg-white border-gray-100 text-gray-500 hover:border-gray-200 hover:text-gray-700'}`\}\s*>\s*<i className="fa-solid fa-book"></i> Registry\s*</button>"""
    replacement = """onClick={() => setActiveTab('GNIDA_REGISTRY')}
                                        className={`flex-none px-4 py-2.5 text-sm font-bold rounded-xl transition-all border snap-start whitespace-nowrap flex items-center gap-2 ${activeTab === 'GNIDA_REGISTRY' ? 'bg-cyan-50 border-cyan-200 text-cyan-700 shadow-sm ring-1 ring-cyan-100' : 'bg-white border-gray-100 text-gray-500 hover:border-gray-200 hover:text-gray-700'}`}
                                    >
                                        <i className="fa-solid fa-book"></i> Registry
                                    </button>"""
    out_text = re.sub(button_pattern, replacement, out_text)

    out_text = out_text.replace("else if (activeTab === 'GNIDA_PTM') currentData =", "else if (activeTab === 'GNIDA_REGISTRY') currentData = gnidaRegistryData;\n                else if (activeTab === 'GNIDA_PTM') currentData =")
    out_text = out_text.replace("else if (activeTab === 'GNIDA_PTM') setGnidaPtmData(prev", "else if (activeTab === 'GNIDA_REGISTRY') setGnidaRegistryData(prev => ({ ...prev, ...loaded }));\n                        else if (activeTab === 'GNIDA_PTM') setGnidaPtmData(prev")
    out_text = out_text.replace("else if (activeTab === 'GNIDA_PTM') setGnidaPtmData(parsed);", "else if (activeTab === 'GNIDA_REGISTRY') setGnidaRegistryData(parsed);\n                        else if (activeTab === 'GNIDA_PTM') setGnidaPtmData(parsed);")
    out_text = out_text.replace("else if (activeTab === 'GNIDA_PTM') { currentData =", "else if (activeTab === 'GNIDA_REGISTRY') { currentData = gnidaRegistryData; name = gnidaRegistryData.projectName || 'Draft'; }\n                else if (activeTab === 'GNIDA_PTM') { currentData =")
    out_text = out_text.replace("activeTab === 'GNIDA_PTM' ? gnidaPtmData :", "activeTab === 'GNIDA_REGISTRY' ? gnidaRegistryData :\n                                                    activeTab === 'GNIDA_PTM' ? gnidaPtmData :")
    
    with open('Madhav_Drafting_Hub.html', 'w', encoding='utf-8') as f:
        f.write(out_text)
    
    print("Injected successfully!")

if __name__ == '__main__':
    main()
