import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

from bs4 import BeautifulSoup

options = webdriver.ChromeOptions()
options.add_argument("headless")

URL = 'https://www.google.com/search?q=%EC%9E%89%EA%B8%80%EB%9E%9C%EB%93%9C+%ED%94%84%EB%A6%AC%EB%AF%B8%EC%96%B4%EB%A6%AC%EA%B7%B8&newwindow=1&hl=en&sxsrf=APq-WBsz-S3latJKQTXbkgBzQL7mtfz7jg%3A1644217659779&source=hp&ei=O8UAYpSzLcz5wQPs6JugDQ&iflsig=AHkkrS4AAAAAYgDTS2bHCWgorUm9gGiTf1MJZq21MVoq&gs_ssp=eJzj4tDP1Tcwii9JNmD0kn8zr_PVjobX8-a8njxH4e2UltfL1rxev-PNtC1AxqvtOwDOLRkE&oq=&gs_lcp=Cgdnd3Mtd2l6EAEYADIHCC4Q6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJ1AAWABghwhoAXAAeACAAQCIAQCSAQCYAQCwAQo&sclient=gws-wiz#sie=lg;/g/11p44qhs93;2;/m/02_tc;mt;fp;1;;'
driver = webdriver.Chrome('/Users/tyflow/Downloads/chromedriver', options=options)
driver.maximize_window()
driver.get(url=URL)
driver.implicitly_wait(10)

posting = driver.find_element_by_xpath(
  '//*[@id="liveresults-sports-immersive__updatable-league-matches"]/div[10]/div[2]/div/table/tbody').find_elements_by_tag_name(
  'tr')

print(len(posting))
trNum = 0
tdNum = 0
for i in range(1, len(posting) + 1):
  if i % 2 == 0:
    trNum = i // 2
    tdNum = 2
  else:
    trNum = i // 2 + 1
    tdNum = 1

  vsUrl = '//*[@id="liveresults-sports-immersive__updatable-league-matches"]/div[10]/div[2]/div/table/tbody/tr[{0}]/td[{1}]/div/div/div/table'.format(
    trNum, tdNum)

  vs_button_check = WebDriverWait(driver, 10).until(EC.presence_of_element_located \
                                                      ((By.XPATH, vsUrl)))
  vs_button = driver.find_element_by_xpath(vsUrl)
  driver.execute_script("arguments[0].click();", vs_button)

  driver.get(url=driver.current_url)
  driver.implicitly_wait(10)


  teamUrl = '//*[@id="liveresults-sports-immersive__match-fullpage"]/div/div[2]/div[4]/div[1]/div/div/div/div/div[1]/div/div[2]/div[1]/div/div[1]/div[2]/div'
  checking = driver.find_elements_by_xpath(teamUrl)
  print(len(checking))
  #
  # try:
  #   team_button_check = WebDriverWait(driver, 10).until(EC.presence_of_element_located \
  #                                                         ((By.XPATH, teamUrl)))
  #   team_button = driver.find_element_by_xpath(teamUrl)
  # except:
  #   teamUrl = '//*[@id="liveresults-sports-immersive__match-fullpage"]/div/div/div[4]/div[1]/div/div/div/div/div[1]/div[1]/div[2]/div[1]/div/div[1]/div[2]/div'
  #   team_button_check = WebDriverWait(driver, 10).until(EC.presence_of_element_located \
  #                                                         ((By.XPATH, teamUrl)))
  #   team_button = driver.find_element_by_xpath(teamUrl)
  #
  # print(team_button.text)
  # driver.execute_script("arguments[0].click();", team_button)

  driver.get(url=URL)
  # driver.implicitly_wait(10)

  # //*[@id="liveresults-sports-immersive__match-fullpage"]/div/div/div[4]/div[1]/div/div/div/div/div[1]/div[1]/div[2]/div[1]
  # //*[@id="liveresults-sports-immersive__match-fullpage"]/div/div[2]/div[4]/div[1]/div/div/div/div/div[1]/div/div[2]/div[1]

# 스코어 없을 때
# //*[@id="liveresults-sports-immersive__match-fullpage"]/div/div[2]/div[4]/div[1]/div/div/div/div/div[1]/div/div[2]/div[1]/div/div[1]/div[2]/div
# 스코어 있을 때
# //*[@id="liveresults-sports-immersive__match-fullpage"]/div/div/div[4]/div[1]/div/div/div/div/div[1]/div[1]/div[2]/div[1]/div/div[1]/div[2]/div
# driver.implicitly_wait(5)
# driver.get(url=driver.current_url)
# posting = driver.find_element_by_xpath('//*[@id="liveresults-sports-immersive__match-fullpage"]/div/div[2]/div[4]/div[1]/div/div/div/div/div[1]/div/div[2]/div[1]/div/div[1]/div[2]/div')
# posting.click()
#
# driver.implicitly_wait(5)
# driver.get(url=driver.current_url)
# for i in range(15):
#   xPath = '//*[@id="liveresults-sports-immersive__updatable-team-matches"]/div[1]/div/table/tbody/tr[{0}]/td[1]/div/div/div/table'.format(i+1)
#   elements = driver.find_elements_by_xpath(xPath)
#   for element in elements:
#       print(element.text)
#
driver.close()
