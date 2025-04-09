from bs4 import BeautifulSoup as bs4
import requests
import time
import pandas as pd
import re

base_url = 'https://job.js88.com/'

list_url = base_url + 'listed_company/list?'

data = {'Name': [], 'URL': [], 'Industry': [], 'Address': []}

start = time.perf_counter()
for i in range(190): # 負荷状況みて増やす Max現状 190
    page_url = list_url + 's=' + str(i + 1)
    res = requests.get(page_url)
    soup = bs4(res.text, "html.parser")

    company_list = soup.find('ul', {'class' : 'result_list'})
    contents = company_list.find_all('li')

    for content in contents:
        elem = content.find('a', {'class' : 'detail_link'})
        if (elem is None): continue
        title = elem.text
        url = content.find('a').get('href')
        industry = content.find('div', {'class': 'co_type'}).text

        # 詳細ページ取得
        detail_page = base_url + url
        detail_res = requests.get(detail_page)
        soup = bs4(detail_res.text, "html.parser")

        section = soup.find('section', {'id': 'sec1'})
        company_info = section.find('dl', {'class' : 'dtl_info'})

        address = company_info.find_all('dd')[5].text
        redirect_url = company_info.find('a').get('href')
        parts = redirect_url.split('url=')
        if (len(parts) > 1) :
            url = parts[1]
            if (re.match(r"^http(?!s)", url)) :
                data['URL'].append(url)
                data['Name'].append(title)
                data['Industry'].append(industry)
                if (re.match(r"^http", address)) :
                    data['Address'].append(company_info.find_all('dd')[4].text)
                else:
                    data['Address'].append(company_info.find_all('dd')[5].text)
    print('done page' + str(i + 1))
    time.sleep(1) #　必要に応じてサーバー負荷軽減のため1秒待つ

df = pd.DataFrame(data)
df.to_excel('http_company_list.xlsx', sheet_name ='上場企業')

end = time.perf_counter()

print('Done list output')
print('{:.2f}'.format((end-start)/60))