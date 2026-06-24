import os
import subprocess
import re

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
    backup_file = 'test_script.jsx.bak'
    if not os.path.exists(backup_file):
        print("Creating backup of test_script.jsx...")
        with open('test_script.jsx', 'r', encoding='utf-8') as f:
            content = f.read()
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(content)
    else:
        print("Backup already exists.")

    with open('test_script.jsx', 'r', encoding='utf-8') as f:
        content = f.read()

    # Step 1: Add age fields to defaultNoidaTransferData
    target_state = "const defaultNoidaTransferData = {"
    new_fields = """const defaultNoidaTransferData = {
                // Age fields added for completeness
                transferor1Age: '',
                transferor2Age: '',
                transferee1Age: '',
                transferee2Age: '',
                transferee3Age: '',
                gpaHolderAge: '',"""
    
    if target_state in content and "transferor1Age:" not in content:
        content = content.replace(target_state, new_fields, 1)
        print("Added age fields to state.")

    # Step 2: Add age inputs to NoidaTransferForm
    # Transferor 1
    t1_father = '<Input label="Father/Spouse Name" name="transferor1Father" value={data.transferor1Father || data.allotteeFather} onChange={(e) => handleSyncChange(e, \'allotteeFather\')} />'
    t1_age = t1_father + '\n                                <Input label="Age (Years)" name="transferor1Age" value={data.transferor1Age} onChange={onChange} />'
    if t1_father in content and "transferor1Age" not in content:
        content = content.replace(t1_father, t1_age, 1)
        print("Added Transferor 1 Age input.")

    # Transferor 2
    t2_father = '<Input label="Father/Spouse Name" name="transferor2Father" value={data.transferor2Father} onChange={onChange} />'
    t2_age = t2_father + '\n                                <Input label="Age (Years)" name="transferor2Age" value={data.transferor2Age} onChange={onChange} />'
    if t2_father in content and "transferor2Age" not in content:
        content = content.replace(t2_father, t2_age, 1)
        print("Added Transferor 2 Age input.")

    # Transferee 1
    tr1_father = '<Input label="Father/Spouse Name" name="transferee1Father" value={data.transferee1Father || data.transfereeFather} onChange={(e) => handleSyncChange(e, \'transfereeFather\')} />'
    tr1_age = tr1_father + '\n                                <Input label="Age (Years)" name="transferee1Age" value={data.transferee1Age} onChange={onChange} />'
    if tr1_father in content and "transferee1Age" not in content:
        content = content.replace(tr1_father, tr1_age, 1)
        print("Added Transferee 1 Age input.")

    # Transferee 2
    tr2_father = '<Input label="Father/Spouse Name" name="transferee2Father" value={data.transferee2Father} onChange={onChange} />'
    tr2_age = tr2_father + '\n                                <Input label="Age (Years)" name="transferee2Age" value={data.transferee2Age} onChange={onChange} />'
    if tr2_father in content and "transferee2Age" not in content:
        content = content.replace(tr2_father, tr2_age, 1)
        print("Added Transferee 2 Age input.")

    # Transferee 3
    tr3_father = '<Input label="Father/Spouse Name" name="transferee3Father" value={data.transferee3Father} onChange={onChange} />'
    tr3_age = tr3_father + '\n                                <Input label="Age (Years)" name="transferee3Age" value={data.transferee3Age} onChange={onChange} />'
    if tr3_father in content and "transferee3Age" not in content:
        content = content.replace(tr3_father, tr3_age, 1)
        print("Added Transferee 3 Age input.")

    # GPA Holder
    gpa_father = '<Input label="Father/Spouse Name" name="gpaHolderFather" value={data.gpaHolderFather} onChange={onChange} />'
    gpa_age = gpa_father + '\n                                <Input label="Age (Years)" name="gpaHolderAge" value={data.gpaHolderAge} onChange={onChange} />'
    if gpa_father in content and "gpaHolderAge" not in content:
        content = content.replace(gpa_father, gpa_age, 1)
        print("Added GPA Holder Age input.")

    with open('test_script.jsx', 'w', encoding='utf-8') as f:
        f.write(content)

    if not compile_check():
        print("Reverting changes due to syntax errors...")
        with open(backup_file, 'r', encoding='utf-8') as f:
            content = f.read()
        with open('test_script.jsx', 'w', encoding='utf-8') as f:
            f.write(content)
        compile_check()

if __name__ == '__main__':
    main()
