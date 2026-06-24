import re
import subprocess

def compile_check():
    print("Running build.py to verify syntax...")
    result = subprocess.run("python build.py", shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print("Compilation failed!")
        print(result.stderr)
        return False
    print("Compilation succeeded!")
    return True

def main():
    with open('test_script.jsx', 'r', encoding='utf-8') as f:
        content = f.read()

    # Step 1: Ensure age fields are in defaultNoidaTransferData
    if "transferor1Age:" not in content:
        pattern = r'(const defaultNoidaTransferData = \{)'
        replacement = r'\1\n                transferor1Age: "",\n                transferor2Age: "",\n                transferee1Age: "",\n                transferee2Age: "",\n                transferee3Age: "",\n                gpaHolderAge: "",'
        content = re.sub(pattern, replacement, content, count=1)
        print("Added age fields to state default.")

    # Step 2: Use regex to add age inputs to NoidaTransferForm
    
    # 1. Transferor 1 Father -> Add Transferor 1 Age
    if 'name="transferor1Age"' not in content:
        pattern = r'(<Input[^>]+?name="transferor1Father".*?/>)'
        replacement = r'\1\n                                <Input label="Age (Years)" name="transferor1Age" value={data.transferor1Age} onChange={onChange} />'
        content = re.sub(pattern, replacement, content, count=1)
        print("Added Transferor 1 Age input.")

    # 2. Transferor 2 Father -> Add Transferor 2 Age
    if 'name="transferor2Age"' not in content:
        pattern = r'(<Input[^>]+?name="transferor2Father".*?/>)'
        replacement = r'\1\n                                <Input label="Age (Years)" name="transferor2Age" value={data.transferor2Age} onChange={onChange} />'
        content = re.sub(pattern, replacement, content, count=1)
        print("Added Transferor 2 Age input.")

    # 3. Transferee 1 Father -> Add Transferee 1 Age
    if 'name="transferee1Age"' not in content:
        pattern = r'(<Input[^>]+?name="transferee1Father".*?/>)'
        replacement = r'\1\n                                <Input label="Age (Years)" name="transferee1Age" value={data.transferee1Age} onChange={onChange} />'
        content = re.sub(pattern, replacement, content, count=1)
        print("Added Transferee 1 Age input.")

    # 4. Transferee 2 Father -> Add Transferee 2 Age
    if 'name="transferee2Age"' not in content:
        pattern = r'(<Input[^>]+?name="transferee2Father".*?/>)'
        replacement = r'\1\n                                <Input label="Age (Years)" name="transferee2Age" value={data.transferee2Age} onChange={onChange} />'
        content = re.sub(pattern, replacement, content, count=1)
        print("Added Transferee 2 Age input.")

    with open('test_script.jsx', 'w', encoding='utf-8') as f:
        f.write(content)

    compile_check()

if __name__ == '__main__':
    main()
