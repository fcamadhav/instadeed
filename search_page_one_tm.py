with open('test_script.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Search for PAGE 1 or Page 1 around 750000 to 790000
pos = 750000
while True:
    pos = content.find("PAGE 1", pos, 790000)
    if pos == -1:
        break
    print(f"PAGE 1 found at index {pos}: {repr(content[pos-50:pos+150])}")
    pos += 6
