from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from utils import Pool, pool_path
from time import time
import os

pool = Pool(pool_path)

if os.path.exists("screenshots"):
    print("Screenshots folder already exists. Please, delete it first.\n")
    os.system("pause")
    exit(0)
os.mkdir("screenshots")

# Configure Chrome WebDriver options
options = Options()
options.add_argument("--window-size=1000,700")
options.add_argument("--start-maximized")
options.add_argument("--headless")
options.add_argument("--disable-gpu")

# Initialize the Chrome WebDriver
driver = webdriver.Chrome(service=Service(executable_path='driver/chromedriver.exe'), options=options)
driver.maximize_window()

start_time = time()
overall_time = 0
counter = 0
for group in pool:
    counter += 1
    print(f"{counter} / {len(pool)}: ", end='')
    processing_time = time()

    # Navigate to the desired URL
    url = f'https://vk.com/club{group.id}'
    driver.get(url)
    driver.implicitly_wait(10)

    # Find the full page element (usually 'body') and capture the screenshot
    full_page = driver.find_element(By.TAG_NAME, "body")
    full_page.screenshot(f"screenshots/{group.screen_name}.png")

    print(f"done ({round(time() - processing_time, 2)}s)")

# Close the browser window
driver.quit()

overall_time = time() - start_time
if overall_time > 60:
    print(f"\nAll the spent time: {int(overall_time // 60)}:{'0' if overall_time % 60 < 10 else ''}{round(overall_time % 60, 2)} s")
else:
    print(f"\nAll the spent time: {round(overall_time, 2)} s")
print(f"Mean time: {round(overall_time / len(pool), 2)} s")
