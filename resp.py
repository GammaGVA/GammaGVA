import requests
from bs4 import BeautifulSoup


def _headrs():
    headers = {'authority': 'www.avito.ru',
              'pragma': 'no-cache',
              'cache-control': 'no-cache',
              'upgrade-insecure-requests': '1',
              'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
              'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
              'sec-fetch-site': 'none',
              'sec-fetch-mode': 'navigate',
              'sec-fetch-user': '?1',
              'sec-fetch-dest': 'document',
              'accept-language': 'ru-RU,ru;q=0.9',
              'cookie': 'Возьми у себя из браузера', }
    return headers


def number_max_page(url):
    resp = requests.get(url=url+'&p=100', headers=_headrs())
    soup = BeautifulSoup(resp.text, 'lxml')
    all_pages = int(soup.find_all('span', class_='pagination-item-JJq_j')[-2].text)
    return all_pages


def reg_pod_links(driver):
    all_links = []
    soup = BeautifulSoup(driver.page_source, 'lxml')
    links = soup.find_all('a', {'data-marker': 'item/grouping'})

    for link in links:
        r = requests.get(url=f'https://www.avito.ru{link.get("href")}', headers=_headrs())
        soup = BeautifulSoup(r.text, 'lxml')
        pod_links = soup.find_all('a', class_='iva-item-sliderLink-uLz1v')
        for pod_link in pod_links:
            all_links.append(f'https://www.avito.ru{pod_link.get("href")}')
    return all_links


def soup_links(driver):
    all_links = []
    soup = BeautifulSoup(driver.page_source, 'lxml')
    links = soup.find_all('a', class_='iva-item-sliderLink-uLz1v')
    for link in links:
        all_links.append(f'https://www.avito.ru{link.get("href")}')
    return all_links
