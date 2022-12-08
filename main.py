from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from resp import number_max_page, reg_pod_links, soup_links
from search_all_info import search_info_apartment_house
import time
import csv


def search_links():
    start = time.time()
    options = webdriver.ChromeOptions()
    options.add_argument(
        'user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36')
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.headless = True
    driver = webdriver.Chrome(
        service=Service("/home/ivan/PycharmProjects/pythonProject/chromedriver"),
        options=options)

    cookie = 'Возьми у себя из браузера'.split(';')

    url = "https://www.avito.ru/voronezh/kvartiry/prodam/novostroyka-ASgBAQICAUSSA8YQAUDmBxSOUg?f=ASgBAQICAUSSA8YQAkDmBxSOUpC~DRSSrjU"

    driver.get(url=url)

    for c in cookie:
        driver.add_cookie({'name': c.split('=')[0].strip(), 'value': c.split('=')[1].strip()})
    # Хотел через pickle записать cookies, но при работе в окне от webdriver никак не могла засчитаться капча.
    # Надо сначала делать запрос, а потом вешать cookies

    all_pages = number_max_page(url=url)
    print(time.time() - start, 'Узнал кол-во страниц.')

    all_links = []

    for number in range(1, all_pages):
        time.sleep(1)
        all_links += soup_links(driver)
        all_links += reg_pod_links(driver)

        all_links = list(set(all_links))
        print(f'Страница {number} закончена')

        driver.find_element(by='xpath', value='//span[@data-marker="pagination-button/next"]').click()
        # Заметил такое, что если номера менять, то много повторений, если прокликивать, то всё тип-топ.

    print(time.time() - start, f'+ собрал все ссылки. До убирания пересечения {len(all_links)}')

    all_links = tuple(set(all_links))

    with open('links.txt', 'w') as file:
        file.writelines(link + '\n' for link in all_links)

    print(time.time() - start, '+ записал все ссылки в текст.')

    driver.close()
    driver.quit()


def search():
    start = time.time()
    options = webdriver.ChromeOptions()
    options.add_argument(
        'user-agent=Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Mobile Safari/537.36')
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.headless = True
    driver = webdriver.Chrome(
        service=Service("/home/ivan/PycharmProjects/pythonProject/chromedriver"),
        options=options)

    cookie = 'Скопируй из браузера.'.split(';')

    url = 'https://www.avito.ru/'

    driver.get(url=url)

    for c in cookie:
        driver.add_cookie({'name': c.split('=')[0].strip(), 'value': c.split('=')[1].strip()})

    with open('/home/ivan/PycharmProjects/pythonProject/GammaGVA/apartments.csv', 'w') as _csv:

        writer = csv.writer(_csv)
        headers = ['url', 'Продавец', 'Тип продавца', 'Статус', 'Цена', 'Цена за метр', 'Адрес', 'Телефон',
                   'Количество комнат', 'Общая площадь', 'Площадь кухни', 'Жилая площадь', 'Этаж', 'Балкон или лоджия',
                   'Высота потолков', 'Санузел', 'Окна', 'Отделка', 'Тип комнат', 'Название новостройки',
                   'Корпус, строение', 'Официальный застройщик', 'Тип участия', 'Срок сдачи', 'Тип дома',
                   'Этажей в доме', 'Пассажирский лифт', 'Грузовой лифт', 'Двор', 'Парковка', 'Способ продажи']
        writer.writerow(headers)

        with open('/home/ivan/PycharmProjects/pythonProject/GammaGVA/links.txt') as txt:

            for link in txt:
                driver.get(url=link)
                writer.writerow(search_info_apartment_house(driver, link).values())

    print(time.time() - start, 'Обработаны все ссылки.')

    driver.close()
    driver.quit()

if __name__=='__main__':

    # search_links()
    search()
