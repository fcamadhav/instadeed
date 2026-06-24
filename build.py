import subprocess
import os
import re

def main():
    print("Step 1: Compiling test_script.jsx to out.js using Babel...")
    babel_bin = os.path.join("node_modules", ".bin", "babel")
    babel_cmd = f"{babel_bin} test_script.jsx --out-file out.js --presets=@babel/preset-react"
    result = subprocess.run(babel_cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print("Babel compilation failed!")
        print("Error details:", result.stderr)
        return
    print("Babel compiled successfully.")

    # Read the current content of Madhav_Drafting_Hub.html
    # If it still has the inline script, we save it as the dev template
    with open('Madhav_Drafting_Hub.html', 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Check if it has the inline text/babel script
    if '<script type="text/babel">' in html_content:
        print("Step 2: Backing up inline dev file to Madhav_Drafting_Hub_dev.html...")
        with open('Madhav_Drafting_Hub_dev.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        dev_content = html_content
    else:
        print("Step 2: Loading structure from Madhav_Drafting_Hub_dev.html...")
        if os.path.exists('Madhav_Drafting_Hub_dev.html'):
            with open('Madhav_Drafting_Hub_dev.html', 'r', encoding='utf-8') as f:
                dev_content = f.read()
        else:
            print("Error: Madhav_Drafting_Hub_dev.html template not found!")
            return

    print("Step 3: Creating optimized production Madhav_Drafting_Hub.html...")
    # Remove the browser Babel compiler library script
    babel_lib_pattern = r'<script src="https://unpkg\.com/@babel/standalone/babel\.min\.js"></script>'
    prod_content = re.sub(babel_lib_pattern, '<!-- Babel compiler library removed in production -->', dev_content)

    # Replace the inline script block with out.js (with cache busting)
    import time
    timestamp = int(time.time())
    inline_script_pattern = r'(<script type="text/babel">)(.*?)(</script>)'
    prod_content, count = re.subn(inline_script_pattern, f'<script src="out.js?v={timestamp}"></script>', prod_content, flags=re.DOTALL)

    if count > 0:
        with open('Madhav_Drafting_Hub.html', 'w', encoding='utf-8') as f:
            f.write(prod_content)
        print("Successfully generated high-performance production Madhav_Drafting_Hub.html.")
    else:
        print("Error: Could not replace inline script block.")

if __name__ == '__main__':
    main()
