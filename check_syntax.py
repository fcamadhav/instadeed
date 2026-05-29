
import re

def check_structure(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract script content
    script_match = re.search(r'<script type="text/babel">(.*?)</script>', content, re.DOTALL)
    if not script_match:
        print("No Babel script found")
        return

    script_content = script_match.group(1)
    
    # Simple brace counting
    open_braces = 0
    lines = script_content.split('\n')
    for i, line in enumerate(lines):
        for char in line:
            if char == '{':
                open_braces += 1
            elif char == '}':
                open_braces -= 1
        
        if open_braces < 0:
            print(f"Error: Excess closing brace at line {i+1} (approx): {line.strip()}")
            return

    if open_braces > 0:
        print(f"Error: Unclosed braces count: {open_braces}")
    else:
        print("Braces seem balanced.")

check_structure(r'c:\Users\fcama\.gemini\antigravity\scratch\madhav-legal-drafter\Madhav_Drafting_Hub.html')
