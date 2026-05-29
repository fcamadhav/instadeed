import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--window-size=1280,1024')

chrome_options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

try:
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('http://localhost:8765/Madhav_Drafting_Hub.html')
    
    print("Waiting 15 seconds for Babel translation...")
    time.sleep(15)
    
    print("=== Console Logs ===")
    for entry in driver.get_log('browser'):
        print(entry)
        
    print("\nSaving screenshot...")
    driver.save_screenshot('browser_render.png')
    
    # Check if root has any children
    has_children = driver.execute_script("return document.getElementById('root').children.length > 0;")
    print(f"React root has children: {has_children}")
    if has_children:
        print("React App rendered successfully!")
        print("Root innerHTML snippet:")
        print(driver.execute_script("return document.getElementById('root').innerHTML.substring(0, 500);"))
        
    driver.quit()
except Exception as e:
    print(f"Error: {e}")
