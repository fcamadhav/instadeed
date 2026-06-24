import base64

img_path = r'C:\Users\fcama\.gemini\antigravity\brain\09be3ae1-8f8d-432b-a4c7-5513355cac8d\instadeed_wordmark_1779465048423.png'
html_path = 'Madhav_Drafting_Hub.html'

# Read and base64-encode the image
with open(img_path, 'rb') as img_file:
    b64_string = base64.b64encode(img_file.read()).decode('utf-8')

# Read the HTML file
with open(html_path, 'r', encoding='utf-8') as html_file:
    html_content = html_file.read()

# Define the target block to replace
target_block = """                                    <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-500 text-white flex items-center justify-center shadow-blue-200 shadow-lg">
                                        <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                                            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                                            <polyline points="14 2 14 8 20 8" />
                                            <polygon points="11 13 8 16 10 16 9 19 12 16 10 16 11 13" fill="currentColor" />
                                        </svg>
                                    </div>
                                    <div>
                                        <h1 className="text-xl font-extrabold text-gray-900 tracking-tight">INSTADEED</h1>
                                    </div>"""

# Define the replacement block
replacement_block = f"""                                    <div className="flex items-center h-10">
                                        <img src="data:image/png;base64,{b64_string}" className="h-8 object-contain" alt="INSTADEED" />
                                    </div>"""

if target_block in html_content:
    updated_content = html_content.replace(target_block, replacement_block)
    with open(html_path, 'w', encoding='utf-8') as html_file:
        html_file.write(updated_content)
    print("Logo embedded successfully!")
else:
    print("Error: Target block not found in HTML file.")
