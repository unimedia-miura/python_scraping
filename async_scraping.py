import asyncio
import aiohttp
from bs4 import BeautifulSoup as bs4
import requests
import time
import pandas as pd
import re

base_url = 'https://job.js88.com/'
list_url = base_url + 'listed_company/list?'
data = {'Name': [], 'URL': [], 'Industry': [], 'Address': []}

async def fetch_detail(session, detail_page_url):
    try:
        async with session.get(detail_page_url) as response:
            html = await response.text()
            soup = bs4(html, "html.parser")
            section = soup.find('section', {'id': 'sec1'})
            if section:
                company_info = section.find('dl', {'class' : 'dtl_info'})
                if company_info:
                    address_element = company_info.find_all('dd')
                    address = address_element[5].text if len(address_element) > 5 else None
                    redirect_url_element = company_info.find('a')
                    redirect_url = redirect_url_element.get('href') if redirect_url_element else None
                    await asyncio.sleep(0.1) # 詳細ページ取得後に非同期スリープ
                    return address, redirect_url
                else:
                    print(f"Error: <dl class='dtl_info'> not found on {detail_page_url}")
                    return None, None
            else:
                print(f"Error: <section id='sec1'> not found on {detail_page_url}")
                return None, None
    except aiohttp.ClientError as e:
        print(f"aiohttp error fetching {detail_page_url}: {e}")
        return None, None
    except Exception as e:
        print(f"An unexpected error occurred on {detail_page_url}: {e}")
        return None, None

def scrape_page(page_num):
    page_url = list_url + 's=' + str(page_num)
    res = requests.get(page_url)
    soup = bs4(res.text, "html.parser")
    company_list = soup.find('ul', {'class' : 'result_list'})
    companies = []
    if company_list:
        contents = company_list.find_all('li')
        for content in contents:
            elem = content.find('a', {'class' : 'detail_link'})
            if (elem):
                title = elem.text
                relative_url = content.find('a').get('href')
                industry = content.find('div', {'class': 'co_type'}).text
                # 詳細ページ取得
                detail_page_url = base_url + relative_url
                companies.append({'title': title, 'industry': industry, 'url': detail_page_url})
    print(f'done page {page_num}')
    time.sleep(0.5) # ページ処理後、次のページ処理までの間に非同期スリープ
    return companies

async def main():
    start = time.perf_counter()
    async with aiohttp.ClientSession(headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'}) as session:
        for i in range(190): # Max 190
            companies = scrape_page(i + 1)
            tasks = [fetch_detail(session, company['url']) for company in companies]
            results = await asyncio.gather(*tasks)
            for j, (address, redirect_url) in enumerate(results):
                if redirect_url:
                    parts = redirect_url.split('url=')
                    if len(parts) > 1:
                        url = parts[1]
                        if re.match(r"^http(?!s)", url):
                            data['Name'].append(companies[j]['title'])
                            data['URL'].append(url)
                            data['Industry'].append(companies[j]['industry'])
                            if address:
                                data['Address'].append(address)
                            else:
                                data['Address'].append(None)

    df = pd.DataFrame(data)
    df.to_excel('http_company_list.xlsx', sheet_name ='上場企業')
    end = time.perf_counter()
    print('Done list output')
    print('{:.2f}'.format((end-start)/60))

if __name__ == "__main__":
    asyncio.run(main())

