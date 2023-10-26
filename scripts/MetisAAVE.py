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
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.support import expected_conditions
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
print(os.environ['TELEGRAM_TOKEN'])
def sendTelegramNotification(text):
   token = os.environ['TELEGRAM_TOKEN']
   chat_id = "1719555198"
   url_req = "https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" + chat_id + "&text=" + text 
   results = requests.get(url_req)
   print(results.json())

# specify the url
url = "https://app.aave.com/reserve-overview/?underlyingAsset=0xdeaddeaddeaddeaddeaddeaddeaddeaddead0000&marketName=proto_metis_v3"

# create a new Chrome browser instance
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# navigate to the url
driver.get(url)

# get the page source
html = driver.page_source

# take screenshot
driver.save_screenshot('screenshot.png')

# get the elements
try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".MuiBox-root:nth-child(2) > .MuiBox-root > .MuiBox-root:nth-child(2) > .MuiBox-root > .MuiBox-root > .MuiTypography-root:nth-child(1)"))
    )
    supplied = element.text
except Exception:
    supplied = None

try:
    totalsupply = driver.find_element(By.CSS_SELECTOR, ".MuiBox-root:nth-child(2) > .MuiBox-root > .MuiBox-root:nth-child(2) .MuiTypography-root:nth-child(3)").text
except Exception:
    totalsupply = None

try:
    borrowed = driver.find_element(By.CSS_SELECTOR, ".MuiBox-root:nth-child(1) > .MuiBox-root:nth-child(1) > .MuiBox-root:nth-child(2) > .MuiBox-root > .MuiBox-root > .MuiTypography-root:nth-child(1)").text
except Exception:
    borrowed = None

try:
    borrowcap = driver.find_element(By.CSS_SELECTOR, ".MuiBox-root:nth-child(1) > .MuiBox-root > .MuiBox-root > .MuiBox-root > .MuiBox-root > .MuiTypography-root:nth-child(3)").text
except Exception:
    borrowcap = None

try:
    apysupply = driver.find_element(By.CSS_SELECTOR, ".MuiBox-root:nth-child(2) > .MuiBox-root > .MuiBox-root:nth-child(3) > .MuiBox-root > .MuiTypography-root").text.replace('\n', '')
except Exception:
    apysupply = None

try:
    apyborrow = driver.find_element(By.CSS_SELECTOR, ".MuiBox-root:nth-child(1) > .MuiBox-root:nth-child(1) > .MuiBox-root:nth-child(3) > .MuiBox-root > .MuiTypography-root").text.replace('\n', '')
except Exception:
    apyborrow = None

try:
    coll = driver.find_element(By.CSS_SELECTOR, ".MuiAlert-message").text
except Exception:
    coll = None


# close the browser window
driver.quit()

now = datetime.now()

# dd/mm/YY H:M:S
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

with open("data/MetisAAVE.csv", "a") as text_file:
    text_file.write(dt_string + "," + str(coll) + "," + str(supplied) +  "," + str(totalsupply) + "," + str(apysupply) + "," + str(borrowed) + "," + str(borrowcap) + "," + str(apyborrow) + '\n')

if coll == None:
    if supplied == None:
        sendTelegramNotification("service is down")
    else:
        sendTelegramNotification("METIS CAN BE USED AS COLLATERAL ON AAVE!!!" + '\n' + "TOTAL SUPPLY: " + str(totalsupply) + '\n' + "TOTAL BORROWED: " + str(borrowed) + '\n' + "SUPPLY APY: " + str(apysupply) + '\n' + "BORROW APY: " + str(apyborrow))
sendTelegramNotification("METIS CAN BE USED AS COLLATERAL ON AAVE!!!" + '\n' + "TOTAL SUPPLY: " + str(totalsupply) + '\n' + "TOTAL BORROWED: " + str(borrowed) + '\n' + "SUPPLY APY: " + str(apysupply) + '\n' + "BORROW APY: " + str(apyborrow))
