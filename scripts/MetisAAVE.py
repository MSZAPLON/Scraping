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
TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']


lserror_IDS = ["5571930248"]
ls_IDS = ["1719555198", "5571930248", "5933851317"]
def sendTelegramNotification(text,ls):
   for chat_id in ls:
      url_req = "https://api.telegram.org/bot" + TELEGRAM_TOKEN + "/sendMessage" + "?chat_id=" + chat_id + "&text=" + text 
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

#convert k to thousand
def convert_k_to_thousand(s):
  if 'K' in s:
    return str(int(float(s.replace('K', '')))*1000)
  else:
    return str(int(float(s)))


# get the elements
try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".MuiBox-root:nth-child(2) > .MuiBox-root > .MuiBox-root:nth-child(2) > .MuiBox-root > .MuiBox-root > .MuiTypography-root:nth-child(1)"))
    )
    supplied = element.text.replace(',', '')
    supplied = convert_k_to_thousand(supplied)
except Exception:
    supplied = None
   
# take screenshot
driver.save_screenshot('screenshot.png')



try:
    price = driver.find_element(By.CSS_SELECTOR, ".css-1x4zjhu:nth-child(1)").text.replace('\n', '').replace(',', '').replace('$', '')
except Exception:
    price = None
   
try:
    totalsupply = driver.find_element(By.CSS_SELECTOR, ".MuiBox-root:nth-child(2) > .MuiBox-root > .MuiBox-root:nth-child(2) .MuiTypography-root:nth-child(3)").text.replace(',', '')
    totalsupply = convert_k_to_thousand(totalsupply)
except Exception:
    totalsupply = None

try:
    borrowed = driver.find_element(By.CSS_SELECTOR, ".MuiBox-root:nth-child(1) > .MuiBox-root:nth-child(1) > .MuiBox-root:nth-child(2) > .MuiBox-root > .MuiBox-root > .MuiTypography-root:nth-child(1)").text.replace(',', '')
    borrowed = convert_k_to_thousand(borrowed)
except Exception:
    borrowed = None


#update supplied
import requests
import json
try:
   result = requests.get('https://andromeda-explorer.metis.io/api?module=account&action=balance&address=0x7314Ef2CA509490f65F52CC8FC9E0675C66390b8')
   print(result.json()['result'])
   allonchain = int(int(result.json()['result'])/1000000000000000000)

   supplied = int(allonchain) + int(float(borrowed))
   print(result)
   print(allonchain)
   print(supplied)
except Exception as e:
   print(f"An exception occurred: {e}")
   print("didnt get the balance")
   
try:
    borrowcap = driver.find_element(By.CSS_SELECTOR, ".MuiBox-root:nth-child(1) > .MuiBox-root > .MuiBox-root > .MuiBox-root > .MuiBox-root > .MuiTypography-root:nth-child(3)").text.replace(',', '')
    borrowcap = convert_k_to_thousand(borrowcap)
except Exception:
    borrowcap = None

try:
    apysupply = driver.find_element(By.CSS_SELECTOR, ".MuiBox-root:nth-child(2) > .MuiBox-root > .MuiBox-root:nth-child(3) > .MuiBox-root > .MuiTypography-root").text.replace('\n', '').replace(',', '').replace('%', '').replace('<', '').replace('>', '')
except Exception:
    apysupply = None

try:
    apyborrow = driver.find_element(By.CSS_SELECTOR, ".MuiBox-root:nth-child(1) > .MuiBox-root:nth-child(1) > .MuiBox-root:nth-child(3) > .MuiBox-root > .MuiTypography-root").text.replace('\n', '').replace(',', '').replace('%', '').replace('<', '').replace('>', '')
except Exception:
    apyborrow = None

try:
    coll = driver.find_element(By.CSS_SELECTOR, ".MuiAlert-message").text.replace(',', '')
except Exception:
    coll = None


# close the browser window
driver.quit()

now = datetime.now()

# dd/mm/YY H:M:S
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

#with open("data/MetisAAVE.csv", "a") as text_file:
#    text_file.write(dt_string + "," + str(coll) + "," + str(supplied) +  "," + str(totalsupply) + "," + str(apysupply) + "," + str(borrowed) + "," + str(borrowcap) + "," + str(apyborrow) + '\n')

#compare the values with the last input
import csv
track = True
if coll == None:
    if supplied == None:
        sendTelegramNotification("service is down",lserror_IDS)
        track = False
    else:
        sendTelegramNotification("METIS CAN BE USED AS COLLATERAL ON AAVE!!!" + '\n' + "TOTAL SUPPLY: " + str(totalsupply) + '\n' + 'SUPPLIED: ' + str(supplied) + '\n' + "TOTAL BORROWED: " + str(borrowcap) + '\n' + "TOTAL BORROWED: " + str(borrowed) + '\n' + "SUPPLY APY: " + str(apysupply) + '\n' + "BORROW APY: " + str(apyborrow),ls_IDS)
if track == True:
    with open('data/MetisAAVE.csv', 'r') as f:
        reader = csv.reader(f)
        header = next(reader)  # skip header
        last_row = None
        for row in reader:
            last_row = row
        if last_row[1:] != [str(coll), str(supplied), str(totalsupply), str(apysupply), str(borrowed), str(borrowcap), str(apyborrow), str(price)]:
            with open("data/MetisAAVE.csv", "a") as text_file:
                text_file.write(str(dt_string) + "," + str(coll) + "," + str(supplied) +  "," + str(totalsupply) + "," + str(apysupply) + "," + str(borrowed) + "," + str(borrowcap) + "," + str(apyborrow) + "," + str(price) + '\n')
        else:
            print('The last row matches the variables in your code.')



