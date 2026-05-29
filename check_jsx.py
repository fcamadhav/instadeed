import re

def check_jsx_tags(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()

    # Simple regex to find HTML/JSX tags
    # We want to match:
    # 1. Self-closing tags: <tag ... />
    # 2. Closing tags: </tag>
    # 3. Opening tags: <tag ...> (excluding comments, expressions, comparisons like a < b)
    # Let's extract JSX blocks from the code or just parse the whole file for potential tags.
    
    # Let's tokenise tags using a regex:
    # This regex matches JSX tags:
    # </?[a-zA-Z][a-zA-Z0-9.-]*(?:\s+[^>]*?)?/?>
    tag_regex = re.compile(r'(</?[a-zA-Z][a-zA-Z0-9.-]*(?:\s+[^>]*?)?/?>|{/\*.*?\*/})')
    
    stack = []
    lines = code.split('\n')
    
    print("Scanning for unclosed JSX tags...")
    for i, line in enumerate(lines, 1):
        # Remove comments, string literals to avoid false positives (simplistic but helpful)
        # For a robust check, let's just find tags on the line
        for match in tag_regex.finditer(line):
            tag_str = match.group(1)
            if tag_str.startswith('{/*') and tag_str.endswith('*/}'):
                continue # ignore JSX comments
                
            # If self-closing, skip
            if tag_str.endswith('/>') or tag_str.startswith('<input') or tag_str.startswith('<img') or tag_str.startswith('<br') or tag_str.startswith('<hr'):
                # Note: in JSX, even <input>, <img>, <br> must be self-closing <input />. But sometimes developers write <br>
                # In React/JSX, <br> without / is actually a syntax error. Let's flag non-self-closing standard empty tags if they are not closed.
                if not tag_str.endswith('/>') and not tag_str.startswith('</'):
                    # In JSX, standard HTML tags like <br>, <img>, <input> MUST be closed or self-closing.
                    # Let's check if the tag name is one of these
                    tag_name = tag_str[1:].split()[0].split('>')[0]
                    # In JSX, these are syntax errors if not closed/self-closing.
                    # Let's push them to stack to see if they get closed, or report them.
                    pass
            
            if tag_str.startswith('</'):
                # Closing tag
                tag_name = tag_str[2:].strip()[:-1].strip()
                if not stack:
                    print(f"Error at line {i}: Closing tag {tag_str} without opening tag")
                else:
                    open_tag, open_line, open_str = stack.pop()
                    if open_tag != tag_name:
                        print(f"Mismatched tag at line {i}: Found {tag_str}, expected closing for {open_str} from line {open_line}")
                        # Put it back or adjust stack to try to recover
                        stack.append((open_tag, open_line, open_str))
            elif tag_str.startswith('<') and not tag_str.endswith('/>'):
                # Opening tag
                # Filter out comparisons like < 5 or JS code with <
                # Tag names should be alphanumeric and start with a letter
                parts = tag_str[1:-1].split()
                if parts:
                    tag_name = parts[0]
                    # Filter out things like <= or other code
                    if re.match(r'^[a-zA-Z][a-zA-Z0-9.-]*$', tag_name):
                        stack.append((tag_name, i, tag_str))
                        
    if stack:
        print("\nUnclosed tags remaining in stack:")
        for tag_name, line, tag_str in reversed(stack):
            print(f"Line {line}: {tag_str}")
    else:
        print("\nAll tags matched!")

if __name__ == '__main__':
    check_jsx_tags('test_script.jsx')
