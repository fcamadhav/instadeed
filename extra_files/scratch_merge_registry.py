import re

def extract_section(text, start_marker, end_marker=None, include_markers=True, regex=False):
    if regex:
        match = re.search(start_marker, text, re.DOTALL)
        if match:
            return match.group(1)
        return ""
    
    start_idx = text.find(start_marker)
    if start_idx == -1: return ""
    
    if end_marker:
        end_idx = text.find(end_marker, start_idx + len(start_marker))
        if end_idx == -1: return ""
        if include_markers:
            return text[start_idx:end_idx + len(end_marker)]
        else:
            return text[start_idx + len(start_marker):end_idx]
    else:
        return text[start_idx:]

with open("Madhav_Drafting_Hub_Final_Registry.html", "r", encoding="utf-8") as f:
    source = f.read()

# 1. State definition
state_regex = r"(const defaultGnidaRegistryData =.*?const \[gnidaRegistryData, setGnidaRegistryData\] = useState\(defaultGnidaRegistryData\);)"
state_code = extract_section(source, state_regex, regex=True)

# 2. Input UI
input_ui_regex = r"(<div className=\"space-y-6\">\s*\{activeTab === 'GNIDA_REGISTRY' && \(.*?)\n                                \}\)\s*\{/\* --- OTHER TABS --- \*/\})"
input_ui = extract_section(source, r"{activeTab === 'GNIDA_REGISTRY' && (", ")}", include_markers=True)
# Wait, basic find might be tricky due to nested brackets. Let's use regex matching carefully or manual line numbers if possible.
