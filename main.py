from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from search_all_info import search_info_apartment_house

options = webdriver.ChromeOptions()
options.add_argument(
    "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")
# options.headless = True
# Для теневой работы добавил - options.headless = True
driver = webdriver.Chrome(
    service=Service("/home/ivan/PycharmProjects/pythonProject/GammaGVA/chromedriver"),
    options=options)

flag_write_headers = True
# Для будущего if-а записи в csv

url = "https://www.avito.ru/voronezh/kvartiry/prodam/1-komnatnye/novostroyka-ASgBAQICAkSSA8YQ5geOUgFAyggUgFk?context=H4sIAAAAAAAA_0q0MrSqLraysFJKK8rPDUhMT1WyLrYyNLNSKk5NLErOcMsvyg3PTElPLVGyrgUEAAD__xf8iH4tAAAA"

driver.get(url=url)
all_pages = int(driver.find_elements(by='class name', value='pagination-item-JJq_j')[-2].text)

for _ in range(all_pages - 1):
    all_links = driver.find_elements(by='class name', value='iva-item-content-rejJg')
    count_links = len(all_links)

    for link in all_links:
        try:
            search_info_apartment_house(link=link, driver=driver, flag_write_headers=flag_write_headers)
        except:
            continue
        # Пока оставлю так, позже добавлю исключения.
        # Решил parser-ить только застройщиков.
        # Ищем лого, в функции добавлю ещё поиск "застройщик"
        driver.implicitly_wait(2)
        driver.close()
        driver.implicitly_wait(2)
        driver.switch_to.window(driver.window_handles[0])

        flag_write_headers = False
        # Внутри функции не поменяешь флаг, а шапку записывать до не комильфо.

    driver.find_elements(by='class name', value='pagination-item-JJq_j')[-1].click()
    """
    У avito фишка такая, они не показывают сколько страниц на самом деле с товаром.
    Надо думать, как находить число страниц.
    Есть вариант в цикл while засунуть, но перед этим найти общее число объявлений и отнимать кол-во ссылок на странице.
    Поставить условие all_ads > 0 и так вот нажимать в цикле - data-marker="pagination-button/next"
    Хотя вот сука когда как, у меня parser нашёл 72 странице, и в браузере столько вижу.
    При переходе на 72 их становится 75.
    Но делаю другой поиск, там 100 страниц, при переходе на 100 их также и осталось.
    Я не понимаю avito, они максимум выводят 5000 объявлений, хотя пишут и 10 000 и 8 000 и 18 000.
    Разобрался, они выводят 100 страниц всегда, искал и по другим городам. Просто группируют похожие объявления,
    если объявлений больше 5к. так что, для пущей статистики, надо либо переходить по ссылки,
    либо просто фиксировать кол-во похожих.
    Надо будет переходить по ним, там цена немного разнится.
    А если parser-ить частников, то предложит сравнить 2-х продавцов,
    и не понятно, будет ли дальше его объявление или нет.
    Решил на частников забить, там и логика меняется, проверены не проверены, собственник не собственник и т.д.
    Как и задумывал, буду parser новостройки, и наверное только от застройщиков.
    Логи в новостройках не меняется, у разных объявлений всё одно и тоже, разного нет.
    parser-ить по новостройкам, с расчётом на то что выведет 100 страниц. Просто придумать условие.
    Надо будет сбор информации в функцию запихнуть, а то при переходе на страницу "похожие объявления шт.
    """

driver.close()
driver.quit()
