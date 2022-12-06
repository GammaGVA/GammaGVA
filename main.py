from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from search_all_info import search_info_apartment_house
from bs4 import BeautifulSoup
import time

options = webdriver.ChromeOptions()
options.add_argument(
    "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")
# options.headless = True
driver = webdriver.Chrome(
    service=Service("/home/ivan/PycharmProjects/pythonProject/GammaGVA/chromedriver"),
    options=options)

flag_write_headers = True
# Для будущего if-а записи в csv

url = "https://www.avito.ru/voronezh/kvartiry/prodam/novostroyka-ASgBAQICAUSSA8YQAUDmBxSOUg?f=ASgBAQICAUSSA8YQAkDmBxSOUpC~DRSSrjU"
driver.get(url=f'{url}&p=100')
soup = BeautifulSoup(driver.page_source, 'lxml')
all_pages = int(soup.find_all('span', class_='pagination-item-JJq_j')[-2].text)
driver.get(url=f'{url}&p=1')
# Перехожу на 100 страницу сразу, что бы узнать кол-во страниц. С супом быстрее.

for _ in range(all_pages - 1):
    all_links = driver.find_elements(by='class name', value='iva-item-content-rejJg')
    alls = time.time()
    for link in all_links:
        try:
            link.find_element(by='class name', value='iva-item-groupingsStep-T_3Y7').click()
            driver.implicitly_wait(2)
            driver.switch_to.window(driver.window_handles[1])

            try:
                pod_all_page = int(driver.find_elements(by='class name', value='pagination-item-JJq_j')[-2].text)
                # Просто не бывает меньше двух
            except:
                pod_all_page = 2

            for __ in range(pod_all_page - 1):

                pod_all_links = driver.find_elements(by='xpath', value='//div[@data-marker="item"]')

                for link2 in pod_all_links:
                    link2.find_element(by='class name', value=f'iva-item-titleStep-pdebR').click()
                    driver.implicitly_wait(2)
                    driver.switch_to.window(driver.window_handles[2])

                    start = time.time()
                    search_info_apartment_house(driver=driver, flag_write_headers=flag_write_headers)
                    print(time.time()-start)

                    driver.close()
                    driver.switch_to.window(driver.window_handles[1])
                try:
                    driver.find_element(by='xpath', value='//span[@data-marker="pagination-button/next"]').click()
                except:
                    continue
                # Это вот до чего я смог додуматься. Поиск не существующего элемента выдаёт ошибку.
                # А это как-то надо обходить. Да и try except работает быстро, в 3.11 вообще обещают моментально.

            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            # Пришлось дублировать из-за того что тут 3 вкладки должно открыться.

            continue
        except:
            # link.find_element(by='xpath', value=f'//div[@data-marker="item-user-logo"]')
            # Передумал так фильтровать застройщиков, т.к. у avito есть своя функция выгрузки только застройщиков.
            # Да и фильтрация по лого так себе. Оказались застройщики без лого. И много агенств с лого.

            link.find_element(by='class name', value=f'iva-item-titleStep-pdebR').click()
            driver.switch_to.window(driver.window_handles[1])

            start = time.time()
            search_info_apartment_house(driver=driver, flag_write_headers=flag_write_headers)
            print(time.time() - start)

            driver.close()
            driver.switch_to.window(driver.window_handles[0])

        flag_write_headers = False
        # Внутри функции не поменяешь флаг, а шапку записывать до не комильфо.
    print(f'!!!{time.time()-alls}!!!')

    driver.find_element(by='xpath', value='//span[@data-marker="pagination-button/next"]').click()

driver.close()
driver.quit()
