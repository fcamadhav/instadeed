import subprocess
import os
import re
import sys
import shutil

def main():
    print("Step 1: Compiling test_script.jsx to out.js using Babel...")
    
    # Check if node is available
    node_exists = shutil.which("node") is not None
    
    if not node_exists:
        print("Warning: 'node' not found. Skipping JSX compilation. Will use existing out.js if present.")
        if not os.path.exists("out.js"):
            print("Error: out.js does not exist and 'node' is not available to compile it!")
            sys.exit(1)
    else:
        babel_bin = os.path.join("node_modules", ".bin", "babel")
        babel_cmd = f"{babel_bin} test_script.jsx --out-file out.js --presets=@babel/preset-react"
        result = subprocess.run(babel_cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print("Babel compilation failed!")
            print("Error details:", result.stderr)
            sys.exit(1)
        print("Babel compiled successfully.")

        # Step 1b: Minifying out.js using Terser
        terser_bin = os.path.join("node_modules", ".bin", "terser")
        if os.path.exists(terser_bin) or shutil.which("terser") is not None:
            print("Step 1b: Minifying out.js using Terser...")
            cmd_path = terser_bin if os.path.exists(terser_bin) else "terser"
            terser_cmd = f"{cmd_path} out.js -o out.js --compress --mangle"
            minify_result = subprocess.run(terser_cmd, shell=True, capture_output=True, text=True)
            if minify_result.returncode != 0:
                print("Terser minification failed! Continuing with unminified bundle.")
                print("Error details:", minify_result.stderr)
            else:
                print("Terser minified out.js successfully.")
        else:
            print("Warning: Terser not found. Bundle will not be minified.")

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

    print("Step 3: Creating self-contained Madhav_Drafting_Hub.html...")
    # Remove the browser Babel compiler library script
    babel_lib_pattern = r'<script src="https://unpkg\.com/@babel/standalone/babel\.min\.js"></script>'
    prod_content = re.sub(babel_lib_pattern, '<!-- Babel compiler library removed in production -->', dev_content)

    # Inline out.js directly into the HTML
    inline_script_pattern = r'(<script type="text/babel">)(.*?)(</script>)'
    with open('out.js', 'r', encoding='utf-8') as f:
        out_js = f.read()
    prod_content, count = re.subn(inline_script_pattern, lambda m: f'<script>{out_js}</script>', prod_content, flags=re.DOTALL)

    if count > 0:
        with open('Madhav_Drafting_Hub.html', 'w', encoding='utf-8') as f:
            f.write(prod_content)
        print(f"Successfully generated self-contained Madhav_Drafting_Hub.html ({len(prod_content)//1024} KB).")
    else:
        print("Error: Could not replace inline script block.")

if __name__ == '__main__':
    main()
