from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime

# specify the url
url = "https://app.aave.com/reserve-overview/?underlyingAsset=0xdeaddeaddeaddeaddeaddeaddeaddeaddead0000&marketName=proto_metis_v3"

import sys
# chrome_options.add_argument("--headless")

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

chrome_service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())

chrome_options = Options()
options = [
    "--headless",
    "--disable-gpu",
    "--window-size=1920,1200",
    "--ignore-certificate-errors",
    "--disable-extensions",
    "--no-sandbox",
    "--disable-dev-shm-usage"
]
for option in options:
    chrome_options.add_argument(option)

driver = webdriver.Chrome(service=chrome_service, options=chrome_options)


# navigate to the url
driver.get(url)

# get the page source
html = driver.page_source

# parse the page source into BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# specify the element to search for
element = '<div class="MuiAlert-message css-1xsto0d">Asset cannot be used as collateral.</div>'

# check if the element is in the page source
if str(soup).find(element) != -1:
    msg = "Asset cannot be used as collateral"
else:
    msg = "NOW NOW NOW"
print(msg)

# close the browser window
driver.quit()

now = datetime.now()

# dd/mm/YY H:M:S
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

with open("data/MetisAAVE.csv", "a") as text_file:
    text_file.write(dt_string + "," + msg + '\n')
