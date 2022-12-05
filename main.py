from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from search_all_info import search_info_apartment_house

options = webdriver.ChromeOptions()
options.add_argument(
    "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")
# options.add_argument("--start-maximized")
# Хотел полноэкранный режим, но при фоновой работе он не работает. Так что координаты среза скриншота подгоняем.
options.headless = True
driver = webdriver.Chrome(
    service=Service("/home/ivan/PycharmProjects/pythonProject/GammaGVA/chromedriver"),
    options=options)

flag_write_headers = True
# Для будущего if-а записи в csv

url = "https://www.avito.ru/voronezh/kvartiry/prodam/novostroyka-ASgBAQICAUSSA8YQAUDmBxSOUg?f=ASgBAQICAUSSA8YQAkDmBxSOUpC~DRSSrjU"
driver.get(url=f'{url}&p=100')
all_pages = int(driver.find_elements(by='class name', value='pagination-item-JJq_j')[-2].text)

driver.get(url=f'{url}&p=1')
# Это было сделано, что бы узнать настоящее кол-во страниц с товаром.
# Думал через while и if сделать, но решил так. Никогда не помешает узнать настоящее кол-во страниц.

for _ in range(all_pages - 1):
    all_links = driver.find_elements(by='class name', value='iva-item-content-rejJg')

    for link in all_links:
        try:
            link.find_element(by='class name', value='iva-item-groupingsStep-T_3Y7').click()
            driver.implicitly_wait(2)
            driver.switch_to.window(driver.window_handles[1])

            try:
                pod_all_page = int(driver.find_elements(by='class name', value='pagination-item-JJq_j')[-2].text)
            except:
                pod_all_page = 2

            for __ in range(pod_all_page - 1):

                pod_all_links = driver.find_elements(by='xpath', value='//div[@data-marker="item"]')

                for link2 in pod_all_links:
                    link2.find_element(by='class name', value=f'iva-item-titleStep-pdebR').click()
                    driver.implicitly_wait(2)
                    driver.switch_to.window(driver.window_handles[2])

                    search_info_apartment_house(driver=driver, flag_write_headers=flag_write_headers)

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
            driver.implicitly_wait(2)
            driver.switch_to.window(driver.window_handles[1])

            search_info_apartment_house(driver=driver, flag_write_headers=flag_write_headers)

            driver.close()
            driver.switch_to.window(driver.window_handles[0])

        flag_write_headers = False
        # Внутри функции не поменяешь флаг, а шапку записывать до не комильфо.

    driver.find_element(by='xpath', value='//span[@data-marker="pagination-button/next"]').click()

driver.close()
driver.quit()
