import subprocess

try:
    res = subprocess.check_output(["git", "log", "-S", "landing.html", "--oneline"], text=True)
    print("Commits referencing landing.html:")
    print(res)
except Exception as e:
    print(f"Error: {e}")
