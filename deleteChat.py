from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests

cookies = {
  'h_selected_employee_no':	'1467738',
  '_gid':	'GA1.2.1934437722.1638144147',
  'cell_company_no':	'9',
  'AUTH_R_TOKEN':	'mNvKWg9KUKGws73UzU1wGXCfnkAw8F',
  'h_selected_company_code':	'biz201703300000011',
  '_ga':	'GA1.2.976419421.1635487891',
  'wehago_s':	'329517655915200600799370545138329421186',
  'h_portal_id':	'jshi25',
  'locale':	'ko',
  'AUTH_A_TOKEN':	'qZtMpehtLeuFlryR0Kxz7PBd6s3c9z',
  'h_selected_company_no':	'9',
  '_gat':	'1'
}

options = Options()
options.add_argument("headless")

driver = webdriver.Chrome('/Users/tyflow/Downloads/chromedriver', chrome_options=options)


url = 'https://www.wehago.com/#/main'

driver.get(url)

for key, value in cookies.items():
        driver.add_cookie({'name': key, 'value': value})

url = 'https://www.wehago.com/#/communication2/talk/1W1mwHUBMZgV-40pGgtA'
driver.get(url)

element = WebDriverWait(driver, 10).until(
  EC.presence_of_element_located((By.CSS_SELECTOR, '.co_balloon_box'))
)
# OjoYYcGqYU5h63Dl3i0tLxMs43yYSWlfYj9oPrbJhaI
# p58qywfPffQVIarpAHvOVApYpo8oRw+UAvdYqgBjQnY=
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')


# data = {'room_id': '1W1mwHUBMZgV-40pGgtA', 'chat_id':'G-z7b30Bqq7xHM_qntKP', 'cno': '9'}
# URL = 'https://api.wehago.com/communication/we-talk/talk-content-del'
# r = requests.post(URL, cookies=cookies, data=data)
#
# print(r)
#

# kuyib30Bqq7xHM_q-sOk