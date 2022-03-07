from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time
from bs4 import BeautifulSoup

options = Options()
# options.add_argument("headless")

driver = webdriver.Chrome('/Users/tyflow/Downloads/chromedriver', chrome_options=options)
url = 'https://sugang.kangwon.ac.kr/login/logout.do'
driver.get(url)

id = '201411893'
password = '*rhrl3131'
logIn = driver.find_element_by_css_selector('#USER_ID')
logIn.send_keys(id)
logIn = driver.find_element_by_css_selector('#PWD')
logIn.send_keys(password)
logIn.send_keys(Keys.RETURN)

while True:
  sugang = '//*[@id="topMnu"]/li[2]/a'
  sugang_button_check = WebDriverWait(driver, 10).until(EC.presence_of_element_located \
                                                        ((By.XPATH, sugang)))
  sugang_button = driver.find_element_by_xpath(sugang)
  driver.execute_script("arguments[0].click();", sugang_button)

  search = '//*[@id="txt_gwamok"]'
  search_input_check = WebDriverWait(driver, 10).until(EC.presence_of_element_located \
                                                        ((By.XPATH, search)))
  search_input = driver.find_element_by_xpath(search)
  search_input.send_keys('데이터통신')

  searchImg = '//*[@id="btn_searchGwamok"]'
  searchImg_button = driver.find_element_by_xpath(searchImg)
  searchImg_button.send_keys(Keys.RETURN)

  num = '//*[@id="gawmok_list"]/tr[1]/td[13]'
  num_text_check = WebDriverWait(driver, 10).until(EC.presence_of_element_located \
                                                        ((By.XPATH, num)))
  num_text = driver.find_element_by_xpath(num).text
  print(num_text)

  if num_text != '61':
    print('오!!!')
    success = '//*[@id="gawmok_list"]/tr[1]/td[1]/button'
    success_button = driver.find_element_by_xpath(success)
    driver.execute_script("arguments[0].click();", success_button)
    print('성공!!!!!!!')
    break


  driver.refresh()

# print(soup.find_all('section'))

  # driver.implicitly_wait(10)

driver.close()