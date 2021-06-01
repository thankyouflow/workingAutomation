from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import sys
from PyQt5.QtWidgets import QLabel, QPushButton, QLineEdit, QFileDialog, QApplication, QCheckBox, QWidget, QMessageBox, QVBoxLayout
from PyQt5.QtCore import QThread, pyqtSignal

class TaskThread(QThread):
    notifyProgress = pyqtSignal()
    def __init__(self, myvar, parent=None):
        QThread.__init__(self, parent)
        self.myvar = myvar

    def run(self):
        self.writing(self.myvar)
        self.notifyProgress.emit()

    def writing(self, myvar):
        id = myvar['id']
        password = myvar['password']
        # 지라에서 데이터 가져오기
        options = Options()
        options.add_argument("headless")

        driver = webdriver.Chrome(myvar['path'], chrome_options=options)
        url = 'http://jira.duzon.com:8080/login.jsp'
        driver.get(url)

        logIn = driver.find_element_by_css_selector('#login-form-username')
        logIn.send_keys(id)
        logIn = driver.find_element_by_css_selector('#login-form-password')
        logIn.send_keys(password)
        logIn.send_keys(Keys.RETURN)
        driver.get(myvar['jira'])
        for num in myvar['check']:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, f'#ghx-pool > div.ghx-swimlane.ghx-first > ul > li:nth-child({str(num)})'))
            )

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            subject = {
                '솔루션': [],
                '설계팀': [],
            }

            context = {
                '솔루션': [],
                '설계팀': [],
            }

            if num == 12:
                index = 28
            elif num == 15:
                index = 31

            for row in soup.select('.ghx-column')[index]:
                issue_key = row['data-issue-key']
                driver.get(f'http://jira.duzon.com:8080/browse/{issue_key}')
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                for title in soup.select('.labels')[0].select('.lozenge'):
                    if title["title"] == '설계':
                        title["title"] += '팀'
                    if title["title"] in subject.keys():
                        if '_' in soup.find_all('h1')[2].get_text():
                            temp = soup.find_all('h1')[2].get_text().split('_')
                            subject[title["title"]].append(temp[0].strip())
                            context[title["title"]].append(
                                soup.select('.wrap')[8].find('div').get_text().strip().replace('조정', '') + temp[1].strip())
                        elif ':' in soup.find_all('h1')[2].get_text():
                            temp = soup.find_all('h1')[2].get_text().split(':')
                            subject[title["title"]].append(temp[0].strip())
                            context[title["title"]].append(
                                soup.select('.wrap')[8].find('div').get_text().strip().replace('조정', '') + temp[1].strip())
                        break

            driver.get(myvar['jira'])

        # 일일업무보고 작성
        options = Options()

        driver = webdriver.Chrome(myvar['path'], chrome_options=options)
        driver.get(myvar['wiki'])
        logIn = driver.find_element_by_css_selector('#os_username')
        logIn.send_keys(id)
        logIn = driver.find_element_by_css_selector('#os_password')
        logIn.send_keys(password)
        logIn.send_keys(Keys.RETURN)

        driver.switch_to.frame("wysiwygTextarea_ifr")

        for i, key in enumerate(subject.keys()):
            write = driver.find_element_by_css_selector(
                f'#tinymce > table.wysiwyg-macro > tbody > tr > td > ol > li:nth-child(6) > ol > li:nth-child({str(i + 1)})')
            write.click()
            for q, row in enumerate(subject[key]):
                write.send_keys(Keys.RETURN)
                if q == 0:
                    write.send_keys(Keys.TAB)
                write.send_keys(row)

            for q, row in enumerate(context[key]):
                write = driver.find_element_by_css_selector(
                    f'#tinymce > table.wysiwyg-macro > tbody > tr > td > ol > li:nth-child(6) > ol > li:nth-child({str(i + 1)}) > ol > li:nth-child({str(q + 1)})')
                write.click()
                write.send_keys(Keys.RETURN)
                write.send_keys(Keys.TAB)
                write.send_keys('[' + Keys.TAB + row[:2] + '[]')
                write.send_keys(Keys.ARROW_LEFT)
                write.send_keys(Keys.BACKSPACE)
                write.send_keys(Keys.ARROW_RIGHT)
                write.send_keys(' ' + row[2:])

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setGeometry(800, 200, 300, 300)
        self.setWindowTitle("일일업무보고 자동화 프로그램")

        self.driverPathLabel = QLabel()
        self.driverPathLabel.setText('chromedriver 경로를 설정해주세요')
        self.driverPathButton = QPushButton("chromedriver 경로")
        self.driverPathButton.clicked.connect(self.driverPathButtonClicked)

        self.idLabel = QLabel()
        self.idLabel.setText('아이디')
        self.idEdit = QLineEdit()

        self.passwordLabel = QLabel()
        self.passwordLabel.setText('비밀번호')
        self.passwordEdit = QLineEdit()
        self.passwordEdit.setEchoMode(QLineEdit.Password)

        self.jiraLabel = QLabel()
        self.jiraLabel.setText('지라 url')
        self.jiraEdit = QLineEdit()

        self.checkLabel = QLabel()
        self.checkLabel.setText('작성할 칸반')
        self.테스트대기_check = QCheckBox('테스트대기')
        self.검수완료_check = QCheckBox('검수완료')

        self.wikiLabel = QLabel()
        self.wikiLabel.setText('wiki 편집 url(작성할 곳)')
        self.wikiEdit = QLineEdit()

        self.targetLabel = QLabel()
        self.targetLabel.setText('몇 번째에 입력하시겠습니까?\n(예시: \'4. 아무개\'일 경우 >  4 )')
        self.targeEdit = QLineEdit()

        self.startButton = QPushButton("작성 시작")


        Box_layout = QVBoxLayout()

        Box_layout.addWidget(self.driverPathButton)
        Box_layout.addWidget(self.driverPathLabel)

        Box_layout.addWidget(self.idLabel)
        Box_layout.addWidget(self.idEdit)

        Box_layout.addWidget(self.passwordLabel)
        Box_layout.addWidget(self.passwordEdit)

        Box_layout.addWidget(self.jiraLabel)
        Box_layout.addWidget(self.jiraEdit)

        Box_layout.addWidget(self.checkLabel)
        Box_layout.addWidget(self.테스트대기_check)
        Box_layout.addWidget(self.검수완료_check)

        Box_layout.addWidget(self.wikiLabel)
        Box_layout.addWidget(self.wikiEdit)

        Box_layout.addWidget(self.targetLabel)
        Box_layout.addWidget(self.targeEdit)

        Box_layout.addWidget(self.startButton)

        self.startButton.clicked.connect(self.onStart)

        self.setLayout(Box_layout)

    def driverPathButtonClicked(self):
        fname = QFileDialog.getOpenFileName(self)
        if fname[0] != '':
            self.driverPathLabel.setText(fname[0])

    def onStart(self):
        checkList = []
        if self.테스트대기_check.isChecked() == True:
            checkList.append(12)

        if self.검수완료_check.isChecked() == True:
            checkList.append(15)

        self.myLongTask = TaskThread(myvar={'id': self.idEdit.text(), 'password': self.passwordEdit.text(), 'jira': self.jiraEdit.text(), 'wiki': self.wikiEdit.text(), 'path': self.driverPathLabel.text(), 'check': checkList})
        self.myLongTask.notifyProgress.connect(self.onProgress)

        self.startButton.setText('작성중')
        self.startButton.setEnabled(False)
        self.myLongTask.start()

    def onProgress(self):
        self.showDialog()
        self.startButton.setText('작성시작')
        self.startButton.setEnabled(True)

    def showDialog(self):
        QMessageBox.information(self, 'Message', '작성이 완료되었습니다.')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()
