import csv
from time import sleep, time
from bs4 import BeautifulSoup


def _info(soup, driver):
    try:
        trader = soup.find('span', {'data-marker': 'seller-info/postfix'}).text
        name_developer = soup.find('span', {'data-marker': 'seller-info/name'}).text
        price = soup.find('span', {'data-marker': 'item-description/price'}).text
        address = soup.find('span', {'data-marker': 'delivery/location'}).text.strip().replace('\n', ' ')
        price_metr2 = soup.find('span', {'data-marker': 'item-description/normalized-price'}).text
        return trader, name_developer, price, address, price_metr2
    except:
        driver.refresh()
        soup = BeautifulSoup(driver.page_source, 'lxml')
        print('Пробую по новой получить информацию.')
        return _info(soup, driver)


def _info_phone(driver):
    driver.find_element(by='class name', value='mav-182h73e').click()
    sleep(1)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    try:
        phone = soup.find('span', {'class': 'Y2vZ1'}).text.strip()
        return phone
    except:
        try:
            phone = ' '.join(soup.find('button', {'class': 'mav-ce0iew'}).text.split()[1:]).strip()
            return phone
        except:
            driver.refresh()
            print('Пробую по новой получить телефон.')
            return _info_phone(driver)


def search_info_apartment_house(driver, url_link):
    start = time()

    soup = BeautifulSoup(driver.page_source, 'lxml')
    trader, name_developer, price, address, price_metr2 = _info(soup, driver)
    info_dict_apartment_house = {'url': url_link,
                                 'Продавец': name_developer,
                                 'Тип продавца': trader,
                                 'Статус': '-',
                                 'Цена': price.replace('\xa0', ' '),
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

    all_info_about_the_apartment = soup.find_all('div', class_='yOvN2')
    for point_info in all_info_about_the_apartment:
        lst_point = point_info.text.split(':')
        info_dict_apartment_house[lst_point[0].strip()] = lst_point[1].strip().replace('\xa0', ' ')

    all_info_the_house = soup.find_all('div', class_='Lehf0')
    for point_info in all_info_the_house:
        lst_point = point_info.text.split(':')
        info_dict_apartment_house[lst_point[0].strip()] = lst_point[1].strip().replace('\xa0', ' ')

    info_dict_apartment_house['Телефон'] = _info_phone(driver)

    print(f'Обработал одну ссылку за {time() - start}.')

    return info_dict_apartment_house
