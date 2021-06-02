from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup

options = Options()
# options.add_argument("headless")

driver = webdriver.Chrome('/Users/tyflow/Downloads/chromedriver', chrome_options=options)
url = 'https://eruri.kangwon.ac.kr/login.php?errorcode=4'
driver.get(url)

id = '201411893'
password = '*rhrl3131'
logIn = driver.find_element_by_css_selector('#input-username')
logIn.send_keys(id)
logIn = driver.find_element_by_css_selector('#input-password')
logIn.send_keys(password)
logIn.send_keys(Keys.RETURN)

url = 'http://eruri.kangwon.ac.kr/course/view.php?id=59190'
driver.get(url)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
link = soup.find_all('ul', 'section img-text')[1].find_all('a')


for i, l in enumerate(link):
    url = l.attrs['href'].replace('view', 'viewer')
    driver.get(url)
    alert_check = False
    try:
        driver.switch_to.alert.accept()
        alert_check = True
    except:
        pass

    time.sleep(2)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    before = soup.find('span', 'jw-text jw-reset jw-text-elapsed')
    minus_list = before.get_text().split(':')
    vedio = driver.find_element_by_css_selector('#vod_player > div.jw-media.jw-reset > video')
    vedio.click()

    time.sleep(2)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    after = soup.find('span', 'jw-text jw-reset jw-text-elapsed')

    if before == after:
        vedio.click()

    time.sleep(5)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    delay_list = soup.find('span', 'jw-text jw-reset jw-text-duration').get_text().split(':')
    delay = (int(delay_list[0]) * 60 + int(delay_list[1])) - (int(minus_list[0]) * 60 + int(minus_list[1]))
    time.sleep(delay)