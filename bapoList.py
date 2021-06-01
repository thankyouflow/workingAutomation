import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import sys

def printProgress (iteration, total, prefix = '', suffix = '', decimals = 1, barLength = 100):
    formatStr = "{0:." + str(decimals) + "f}"
    percent = formatStr.format(100 * (iteration / float(total)))
    filledLength = int(round(barLength * iteration / float(total)))
    bar = '#' * filledLength + '-' * (barLength - filledLength)
    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percent, '%', suffix)),
    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()

def crawling():
    user = 'jshi25'
    pw = 'jshi25'

    sess = requests.session()

    login = {
        'os_username': user,
        'os_password': pw
    }

    query_url = 'http://wiki.duzon.com:8080/plugins/viewsource/viewpagesrc.action?pageId=43142565'
    res = sess.post(query_url, data=login)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, 'html.parser')
    query = str(soup.find_all('img')[4]).split('|')[1].replace('개인조정', '개인조정, 법인조정').replace('jqlQuery', 'jql')

    total_url = 'http://jira.duzon.com:8080/issues/?' + query
    res = sess.post(total_url, data=login)

    soup = BeautifulSoup(res.text, 'html.parser')

    except_list = ['back', 'backend', 'BACK']
    contain_list = ['front', 'front/back', 'Front', 'FRONT']
    result_list = []
    issue_list = soup.find_all('span', {'class':'issue-link-key'})
    for i, key in enumerate(issue_list):
        key_url = f'http://jira.duzon.com:8080/browse/{key.get_text()}'
        res = sess.get(key_url)
        soup = BeautifulSoup(res.text, 'html.parser')
        back_check = False
        for title in soup.select('.labels')[0].select('.lozenge'):
            if title.get_text() in except_list:
                back_check = True
            elif title.get_text() in contain_list:
                back_check = False
                break

        if not back_check:
            p = re.compile('[a-zA-Z]{4}[0-9]{4}')
            menu_id = p.findall(soup.select('.aui-label')[0].get_text())[0]
            if menu_id not in result_list:
                result_list.append(menu_id)

        printProgress(i, len(issue_list) - 1, '제작중:', f'{i + 1}/{len(issue_list)}', 1, 50)

    return result_list

print('front 배포리스트(개인, 법인) 제작을 시작하겠습니다.\n')

today = str(datetime.today()).split(' ')[0]
result = crawling()
print(f'\nfront 배포리스트(개인, 법인) {len(result)}개 {today}\n')
for res in result:
    print(res)
print('\nfront 배포리스트(개인, 법인) 제작이 완료되었습니다.')
print('예외 케이스가 존재할 수 있으니 반드시 확인해주세요!')

