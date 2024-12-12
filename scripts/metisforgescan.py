from bs4 import BeautifulSoup
from datetime import datetime
import requests
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']

lserror_IDS = ["5571930248"]
ls_IDS = ["5571930248"]

def sendTelegramNotification(text, ls):
    for chat_id in ls:
        url_req = "https://api.telegram.org/bot" + TELEGRAM_TOKEN + "/sendMessage" + "?chat_id=" + chat_id + "&text=" + text 
        results = requests.get(url_req)
        print(results.json())

# specify the url
url = "https://metisforge.io/"
search_text = "CrazyPug"

# create a new Chrome browser instance
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# navigate to the url
driver.get(url)

# Check for the element with specific text
try:
    elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h2.MuiTypography-root.MuiTypography-h2.mui-20q20i"))
    )
    element_text = None
    for element in elements:
        if element.text == search_text:
            element_text = element.text
            break
except Exception:
    element_text = None

# close the browser window
driver.quit()

# Send Telegram notification based on the presence of the element
if element_text == search_text:
    sendTelegramNotification(f"{search_text} is now available on the website.", ls_IDS)
else:
    sendTelegramNotification(f"{search_text} is NOT available on the website.", lserror_IDS)
