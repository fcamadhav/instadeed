import os

def search_rohan():
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith(('.html', '.js', '.css', '.md')):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        for i, line in enumerate(f, 1):
                            if 'Rohan' in line:
                                print(f"{path} [Line {i}]: {line.strip()}")
                except Exception as e:
                    pass

if __name__ == '__main__':
    search_rohan()
