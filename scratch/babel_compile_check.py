import re
import subprocess
import os

def check_babel_compile(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract Babel script
    match = re.search(r'<script type="text/babel">(.*?)</script>', content, re.DOTALL)
    if not match:
        print("No Babel script found")
        return
        
    script = match.group(1)
    
    # Write to a temp jsx file
    temp_jsx = 'scratch/temp_code.jsx'
    os.makedirs('scratch', exist_ok=True)
    with open(temp_jsx, 'w', encoding='utf-8') as f:
        f.write(script)
        
    print("Running local Babel compilation check...")
    # Run npx babel
    result = subprocess.run(
        ['npx', 'babel', temp_jsx, '--presets', '@babel/preset-react', '--out-file', 'scratch/temp_code_compiled.js'],
        capture_output=True,
        text=True,
        shell=True
    )
    
    if result.returncode != 0:
        print("BABEL COMPILATION FAILED!")
        print("STDERR:")
        print(result.stderr)
        print("STDOUT:")
        print(result.stdout)
    else:
        print("BABEL COMPILATION SUCCEEDED! The code compiles perfectly.")

if __name__ == '__main__':
    check_babel_compile('Madhav_Drafting_Hub.html')
