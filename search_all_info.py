from easyocr import Reader
import csv
from os import remove


def search_info_apartment_house(link, driver, flag_write_headers):

    link.find_element(by='xpath', value=f'//div[@data-marker="item-user-logo"]')

    url_link = link.find_element(by='xpath', value=f'//div/div[2]/div[2]/a').get_attribute('href')

    link.find_element(by='class name', value=f'iva-item-titleStep-pdebR').click()
    driver.implicitly_wait(2)
    driver.switch_to.window(driver.window_handles[1])

    name_developer = driver.find_element(by='class name', value='text-size-ms-_Zk4a').text
    price = driver.find_element(by='class name', value='text-size-xxl-UPhmI').text.strip()
    description = driver.find_element(by='class name', value='style-item-description-html-qCwUL').text.strip().replace(
        '\n', ' ')
    address = driver.find_element(by='class name', value='style-item-address-KooqC').text.strip().replace('\n', ' ')
    price_metr2 = driver.find_element(by='class name', value='style-item-price-sub-price-_5RUD').text.strip()

    driver.find_element(by='xpath', value='//button[@data-marker="item-phone-button/card"]').click()
    driver.implicitly_wait(2)

    link_phone_img = driver.find_element(by='class name', value='item-popup-phoneImage-adVhz').get_attribute('src')

    driver.get(url=link_phone_img)
    driver.implicitly_wait(2)
    driver.save_screenshot(filename='/home/ivan/PycharmProjects/pythonProject/phone.png')
    driver.back()

    phone: list = Reader(['ru']).readtext('/home/ivan/PycharmProjects/pythonProject/phone.png', detail=0)

    all_info_about_the_apartment = driver.find_elements(by='class name', value='params-paramsList__item-appQw')
    info_dict_apartment_house = {'url': url_link,
                                 'Застройщик': name_developer,
                                 'Цена': price,
                                 'Цена за метр': price_metr2,
                                 'Адрес': address,
                                 'Телефон': ' '.join(phone),
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
                                 'Способ продажи': '-',
                                 'Описание': description}

    for point_info in all_info_about_the_apartment:
        lst_point = point_info.text.split(':')
        info_dict_apartment_house[lst_point[0].strip()] = lst_point[1].strip()

    all_info_the_house = driver.find_elements(by='class name', value='style-item-params-list-item-aXXql')
    for point_info in all_info_the_house:
        lst_point = point_info.text.split(':')
        info_dict_apartment_house[lst_point[0].strip()] = lst_point[1].strip()

    remove('/home/ivan/PycharmProjects/pythonProject/phone.png')
    # Удаляем скриншот.

    keys = []
    values = []

    for key, value in info_dict_apartment_house.items():
        keys.append(key)
        values.append(value)

    with open('apartment.csv', 'a') as f_csv:
        writer = csv.writer(f_csv)

        if flag_write_headers:
            writer.writerow(keys)

        writer.writerow(values)
