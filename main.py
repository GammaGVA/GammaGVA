from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from easyocr import Reader
import csv
from os import remove

options = webdriver.ChromeOptions()
options.add_argument(
    "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(
    service=Service("/home/ivan/PycharmProjects/pythonProject/GammaGVA/chromedriver"),
    options=options
)

driver.get(
    url="https://www.avito.ru/voronezh/kvartiry/prodam/1-komnatnye/novostroyka-ASgBAQICAkSSA8YQ5geOUgFAyggUgFk?context=H4sIAAAAAAAA_0q0MrSqLraysFJKK8rPDUhMT1WyLrYyNLNSKk5NLErOcMsvyg3PTElPLVGyrgUEAAD__xf8iH4tAAAA")
all_links = driver.find_elements(by='class name', value='iva-item-content-rejJg')
count_links = len(all_links)

for link in range(1, count_links + 1):
    try:
        driver.find_element(by='xpath', value=f'/html/body/div[1]/div/div[3]/div[3]/div[3]/div[5]/div[2]/div[{link}]/div/div[3]/div/div[1]/div[1]/a')
        # Этим делаю отбор только застройщиков.
    except:
        continue

    url_link = driver.find_element(by='xpath',value=f'/html/body/div[1]/div/div[3]/div[3]/div[3]/div[5]/div[2]/div[{link}]/div/div[2]/div[2]/a').get_attribute('href')

    driver.find_element(by='xpath', value=f'/html/body/div[1]/div/div[3]/div[3]/div[3]/div[5]/div[2]/div[{link}]/div/div[2]/div[2]/a').click()
    # Абсолютно тупой способ, но работает. Пока не понял как из уже найденного all_links дальше найти.
    # Пробовал по-разному, но он мне 50 одинаковых ссылок выдавал.
    # Надо что-то с этим делать, а то лишние запросы провожу тогда.
    # try except справляется, и вроде как они работают быстрее чем if, но это не дело.
    driver.implicitly_wait(2)
    driver.switch_to.window(driver.window_handles[1])

    neme_devoloper = driver.find_element(by='class name', value='text-size-ms-_Zk4a').text
    price = driver.find_element(by='class name', value='text-size-xxl-UPhmI').text.strip()
    description = driver.find_element(by='class name', value='style-item-description-html-qCwUL').text.strip().replace('\n', ' ')
    address = driver.find_element(by='class name', value='style-item-address-KooqC').text.strip().replace('\n', ' ')
    price_metr2 = driver.find_element(by='class name', value='style-item-price-sub-price-_5RUD').text.strip()

    driver.find_element(by='xpath', value='/html/body/div[1]/div/div[2]/div/div[3]/div[4]/div[2]/div[1]/div[1]/div/div[2]/div[1]/div/div/div[1]/span/span/div/div/button').click()
    # driver.find_element(by='xpath', value='//div[@data-marker="item-phone-button/card"]').click()
    driver.implicitly_wait(2)
    link_phone_img = driver.find_element(by='class name', value='item-popup-phoneImage-adVhz').get_attribute('src')
    driver.get(url=link_phone_img)
    driver.implicitly_wait(2)
    driver.save_screenshot(filename='/home/ivan/PycharmProjects/pythonProject/phone.png')
    driver.back()
    # Я так и не нашёл способа без скачивания, распознать текст.
    # Так же информация как скачать из seleniuma прошла мимо
    # Теперь вот скришотом.
    # Можно было бы не переходить на ссылку картинки и так скриншот сделать. Но не хотелесь с координатами скриншота возиться.

    phone: list = Reader(['ru']).readtext('/home/ivan/PycharmProjects/pythonProject/phone.png', detail=0)

    # Не видит карту при установленном cuda, и process finished with exit code 132 (interrupted by signal 4 sigill) при распозновании
    # Решение пока не нашёл, на форумах написано, такое при не соответствии архитектуры - устранил.

    all_info_about_the_apartment = driver.find_elements(by='class name', value='params-paramsList__item-appQw')
    info_dict_apartment_house = {'url': url_link,
                                 'Застройщик': neme_devoloper,
                                 'Цена': price,
                                 'Цена за метр': price_metr2,
                                 'Адрес': address,
                                 'Описание': description,
                                 'Телефон': ' '.join(phone),
                                 'Количество комнат': 'Данных не представлялись',
                                 'Общая площадь': 'Данные не предоставлены',
                                 'Площадь кухни': 'Данные не предоставлены',
                                 'Жилая площадь': 'Данные не предоставлены',
                                 'Этаж': 'Данные не предоставлены',
                                 'Балкон или лоджия': 'Данные не предоставлены',
                                 'Высота потолков': 'Данные не предоставлены',
                                 'Санузел': 'Данные не предоставлены',
                                 'Окна': 'Данные не предоставлены',
                                 'Отделка': 'Данные не предоставлены',
                                 'Тип комнат': 'Данные не предоставлены',
                                 'Название новостройки': 'Данные не предоставлены',
                                 'Корпус, строение': 'Данные не предоставлены',
                                 'Официальный застройщик': 'Данные не предоставлены',
                                 'Тип участия': 'Данные не предоставлены',
                                 'Срок сдачи': 'Данные не предоставлены',
                                 'Тип дома': 'Данные не предоставлены',
                                 'Этажей в доме': 'Данные не предоставлены',
                                 'Пассажирский лифт': 'Данные не предоставлены',
                                 'Грузовой лифт': 'Данные не предоставлены',
                                 'Двор': 'Данные не предоставлены',
                                 'Парковка': 'Данные не предоставлены',
                                 'Способ продажи': 'Данные не предоставлены'}
    # А может сделать тогда один большой словарь, квартира и дом.
    # Да и сразу все данные найденные ранее воткнуть сюда. Как раз сгрупирую всё как положено.
    # Это должны быть все варианты, теперь только сгрупировать.

    for point_info in all_info_about_the_apartment:
        lst_point = point_info.text.split(':')
        info_dict_apartment_house[lst_point[0].strip()] = lst_point[1].strip()

    all_info_the_house = driver.find_elements(by='class name', value='style-item-params-list-item-aXXql')
    for point_info in all_info_the_house:
        lst_point = point_info.text.split(':')
        info_dict_apartment_house[lst_point[0].strip()] = lst_point[1].strip()

    remove('/home/ivan/PycharmProjects/pythonProject/phone.png')
    # Удаляем скриншот.

    # Начал думать с записью в csv и встрял. Все словари разные.
    # Разное количество столбцов, да и встречаются разные типы данных.
    # Где-то указан потолок, но не отделки, где-то отделка, но нет этажа, или тиа планировки.
    # Информации по поводу записи по названиям столбцов в csv не нашёл. Попробую ещё поискать.
    # Как обходное решение, думаю создать словарь, с важными категориями и значением None.
    # А уже при парсинге забивать значения, туда где они есть.

    driver.implicitly_wait(2)
    driver.close()
    driver.implicitly_wait(2)
    driver.switch_to.window(driver.window_handles[0])
