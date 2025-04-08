from bs4 import BeautifulSoup as bs4
import requests
import time
import pandas as pd

base_url = 'https://comsite.jp/'

data = {'Name': [], 'URL': [], 'Industry': []}
# for i in range(10):
# url = base_url + str(i + 1)
res = requests.get(base_url)
soup = bs4(res.text, "html.parser")

content = soup.find('div', {'id' : 'content'})
article_list = content.find_all('article')

for article in article_list:
    title = article.find('header').find('h2').text
    url = article.find('footer').find('a').get('href')
    date = article.find('header').find('a').text

    data['Name'].append(title)
    data['URL'].append(url)
    data['Industry'].append(date)

# print('done page' + str(i + 1))
# time.sleep(2) #　サーバー負荷軽減のため２秒待つ

df = pd.DataFrame(data)
df.to_excel('list_data.xlsx', sheet_name ='東証プライム')
print('Done list output')