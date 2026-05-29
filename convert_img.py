
import base64
import os

def image_to_base64(path):
    try:
        with open(path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            return f"data:image/png;base64,{encoded_string}"
    except FileNotFoundError:
        return None

base64_str = image_to_base64("GNIDA_logo.png")
if base64_str:
    # Print only the first 100 chars and last 20 to verify, writing full to a temp file
    # actually better to just write it to a text file I can read with view_file
    with open("gnida_logo_base64.txt", "w") as f:
        f.write(base64_str)
    print("Successfully converted and saved to gnida_logo_base64.txt")
else:
    print("File not found.")
