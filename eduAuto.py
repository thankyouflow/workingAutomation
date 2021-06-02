from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup

options = Options()
# options.add_argument("headless")

driver = webdriver.Chrome('/Users/tyflow/Downloads/chromedriver', chrome_options=options)
url = 'https://ict.douzoneedu.co.kr/douzone/member/login.asp'
driver.get(url)

id = 'jshi25'
password = '*rhrl3131'
logIn = driver.find_element_by_css_selector('#userID')
logIn.send_keys(id)
logIn = driver.find_element_by_css_selector('#userPass')
logIn.send_keys(password)
logIn.send_keys(Keys.RETURN)
url = 'https://ict.douzoneedu.co.kr/douzone/mypage/class_room_hrd.asp'
driver.get(url)
study = driver.find_element_by_css_selector('#myc_cont_area > div > ul > li > a > span.cbtn')
study.click()
time.sleep(2)
driver.switch_to.window(driver.window_handles[1])
study = driver.find_element_by_css_selector('#dashboard > div.main_container > div.back_leftmenu > ul > li.icon_study')
study.click()

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
count = len(soup.find('table', 'tb_01 txt_cen mgt_10').find_all('tr')) - 1
for i in range(count):
    url = f'http://ict.douzoneedu.co.kr/Campus/student/classroom/EnterClass.asp?txtChapterid=1&txtSyllabusno={(i + 1) * 2}&txtFrame_amt=1&txtSectionId=1&txtprocess=0'
    driver.get(url)
    if i != 0:
        driver.switch_to.alert.accept()
    time.sleep(4)
    driver.switch_to.frame(driver.find_element_by_css_selector("body > iframe"))
    driver.switch_to.frame(driver.find_element_by_css_selector("html > frameset > frame:nth-child(2)"))
    move = driver.find_element_by_css_selector('#mediaControl > div.playback > li.playBtn > a')
    move.click()

    time.sleep(2)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    num = int(soup.find('div', 'totalPageNum').get_text()) - int(soup.find('div', 'pageNum').get_text())

    if num == 0:
        time_list = soup.find('div', 'timertotal').get_text().split(':')
        delay = int(time_list[0]) * 60 + int(time_list[1])
        time.sleep(delay + 1)

    for i in range(num):
        time_list = soup.find('div', 'timertotal').get_text().split(':')
        delay = int(time_list[0]) * 60 + int(time_list[1])
        time.sleep(delay)
        move = driver.find_element_by_css_selector('#bottom > div.pageControl > div.nextBtn > a')
        move.click()
        time.sleep(2)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')