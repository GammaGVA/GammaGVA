from easyocr import Reader
import csv
from time import sleep
from bs4 import BeautifulSoup

def _info(soup):
    try:
        trader = soup.find('div', {'data-marker': 'seller-info/label'}).text
        name_developer = soup.find('span', class_='text-size-ms-_Zk4a').text
        price = soup.find('span', class_='text-size-xxl-UPhmI').text
        address = soup.find('div', class_='style-item-address-KooqC').text.strip().replace('\n', ' ')
        price_metr2 = soup.find('div', class_='style-item-price-sub-price-_5RUD').text
        return trader, name_developer, price, address, price_metr2
    except:
        print('Ошибка получения информации.')
        return _info(soup)

def _info_phone(soup, driver):
    try:
        sleep(1)
        link_phone = soup.find('img', class_='item-popup-phoneImage-adVhz').get('src')
        driver.get(url=link_phone)
        driver.save_screenshot(filename='/home/ivan/PycharmProjects/pythonProject/phone.png')
        driver.back()
        phone = ' '.join(Reader(['ru']).readtext('/home/ivan/PycharmProjects/pythonProject/phone.png', detail=0))
        return phone
    except:
        print('Ошибка получения телефона.')
        return _info_phone(soup, driver)
def search_info_apartment_house(driver, flag_write_headers):
    url_link = driver.current_url
    soup = BeautifulSoup(driver.page_source, 'lxml')
    trader, name_developer, price, address, price_metr2 = _info(soup)
    info_dict_apartment_house = {'url': url_link,
                                 'Застройщик': name_developer,
                                 'Цена': price.replace('\xa0', ' '),
                                 'Продавец': trader,
                                 'Цена за метр': price_metr2.replace('\xa0', ' '),
                                 'Адрес': address,
                                 'Телефон': '-',
                                 'Количество комнат': '-',
                                 'Общая площадь': '-',
                                 'Площадь кухни': '-',
                                 'Жилая площадь': '-',
                                 'Этаж': '-',
                                 'Балкон или лоджия': '-',
                                 'Высота потолков': '-',
                                 'Санузел': '-',
                                 'Окна': '-',
                                 'Отделка': '-',
                                 'Тип комнат': '-',
                                 'Название новостройки': '-',
                                 'Корпус, строение': '-',
                                 'Официальный застройщик': '-',
                                 'Тип участия': '-',
                                 'Срок сдачи': '-',
                                 'Тип дома': '-',
                                 'Этажей в доме': '-',
                                 'Пассажирский лифт': '-',
                                 'Грузовой лифт': '-',
                                 'Двор': '-',
                                 'Парковка': '-',
                                 'Способ продажи': '-'}

    all_info_about_the_apartment = soup.find_all('li', class_='params-paramsList__item-appQw')
    for point_info in all_info_about_the_apartment:
        lst_point = point_info.text.split(':')
        info_dict_apartment_house[lst_point[0].strip()] = lst_point[1].strip().replace('\xa0', ' ')

    all_info_the_house = soup.find_all('li', class_='style-item-params-list-item-aXXql')
    for point_info in all_info_the_house:
        lst_point = point_info.text.split(':')
        info_dict_apartment_house[lst_point[0].strip()] = lst_point[1].strip().replace('\xa0', ' ')

    driver.find_element(by='xpath', value='//button[@data-marker="item-phone-button/card"]').click()
    sleep(1)

    soup = BeautifulSoup(driver.page_source, 'lxml')

    info_dict_apartment_house['Телефон'] = _info_phone(soup, driver)

    with open('apartments.csv', 'a') as f_csv:
        writer = csv.DictWriter(f_csv, fieldnames=info_dict_apartment_house.keys())

        if flag_write_headers:
            writer.writeheader()

        writer.writerow(info_dict_apartment_house)
