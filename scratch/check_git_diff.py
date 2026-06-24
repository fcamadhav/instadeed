import subprocess

# Run git log to see what commits modified the root route in server.py
commits = subprocess.check_output(["git", "log", "-n", "10", "--oneline"], text=True)
print("Recent commits:")
print(commits)

# Get diff of server.py for the last commit
diff = subprocess.check_output(["git", "show", "73eeb05", "--", "server.py"], text=True)
for line in diff.split("\n"):
    if "@app.get(\"/\")" in line or "@app.get('/')" in line or "serve_frontend" in line or "landing.html" in line:
        print(line)
