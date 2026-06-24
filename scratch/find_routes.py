with open("server.py", "r", encoding="utf-8") as f:
    for idx, line in enumerate(f):
        if "@app." in line or "HTMLResponse" in line or "FileResponse" in line:
            print(f"{idx+1}: {line.strip()}")
