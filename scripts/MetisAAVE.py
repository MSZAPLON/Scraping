from bs4 import BeautifulSoup
from datetime import datetime


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

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

# parse the page source into BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# specify the elements to search for
element1 = '<div class="MuiAlert-message css-1xsto0d">Asset cannot be used as collateral.</div>'
element2 = '<p class="MuiTypography-root MuiTypography-main16 MuiTypography-noWrap css-1ogi1pb">'
element3 = '<span class="MuiCircularProgress-root MuiCircularProgress-determinate MuiCircularProgress-colorSuccess css-1hz1jwd" role="progressbar" aria-valuenow="'

# check if the elements are in the page source
if str(soup).find(element1) != -1:
    msg1 = "Asset cannot be used as collateral"
else:
    msg1 = "NOW NOW NOW"

start2 = str(soup).find(element2)
if start2 != -1:
    end2 = str(soup).find('</p>', start2)
    msg2 = str(soup)[start2+len(element2):end2]
else:
    msg2 = "Element not found"

start3 = str(soup).find(element3)
if start3 != -1:
    end3 = str(soup).find('"', start3+len(element3))
    msg3 = str(soup)[start3+len(element3):end3]
else:
    msg3 = "Element not found"

print(msg1)
print(msg2)
print(msg3)

# close the browser window
driver.quit()

now = datetime.now()

# dd/mm/YY H:M:S
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

with open("data/MetisAAVE.csv", "a") as text_file:
    text_file.write(dt_string + "," + msg1 + "," + msg2 + "," + msg3 + '\n')
