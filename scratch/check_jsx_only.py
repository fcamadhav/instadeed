import re

def check_jsx_only(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract Babel script
    match = re.search(r'<script type="text/babel">(.*?)</script>', content, re.DOTALL)
    if not match:
        print("No Babel script found")
        return
        
    script = match.group(1)
    
    # Regex to match JSX tags and comments
    # Matches:
    # 1. Self-closing tags: <Tag ... />
    # 2. Closing tags: </Tag>
    # 3. Opening tags: <Tag ...> (excluding comparisons)
    tag_regex = re.compile(r'(</?[A-Z][a-zA-Z0-9.-]*(?:\s+[^>]*?)?/?>|{/\*.*?\*/})')
    
    stack = []
    lines = script.split('\n')
    
    for i, line in enumerate(lines, 1):
        for match in tag_regex.finditer(line):
            tag_str = match.group(1)
            if tag_str.startswith('{/*'):
                continue
                
            if tag_str.endswith('/>'):
                continue # self-closing
                
            if tag_str.startswith('</'):
                tag_name = tag_str[2:].strip()[:-1].strip()
                if not stack:
                    print(f"Error at line {i}: Closing tag {tag_str} without opening tag")
                else:
                    open_tag, open_line, open_str = stack.pop()
                    if open_tag != tag_name:
                        print(f"Mismatched tag at line {i}: Found {tag_str}, expected closing for {open_str} from line {open_line}")
                        stack.append((open_tag, open_line, open_str))
            else:
                # Opening tag
                parts = tag_str[1:-1].split()
                if parts:
                    tag_name = parts[0]
                    if re.match(r'^[A-Z][a-zA-Z0-9.-]*$', tag_name):
                        stack.append((tag_name, i, tag_str))
                        
    if stack:
        print("Unclosed React/JSX components in stack:")
        for tag_name, line, tag_str in reversed(stack):
            print(f"Line {line}: {tag_str}")
    else:
        print("React/JSX components are perfectly balanced!")

if __name__ == '__main__':
    check_jsx_only('Madhav_Drafting_Hub.html')
