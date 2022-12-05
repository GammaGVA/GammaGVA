from easyocr import Reader
import csv
from PIL import Image
from time import sleep


def search_info_apartment_house(driver, flag_write_headers):
    try:
        url_link = driver.current_url
        trader = driver.find_element(by='xpath', value='//div[@data-marker="seller-info/label"]').text
        name_developer = driver.find_element(by='class name', value='text-size-ms-_Zk4a').text
        price = driver.find_element(by='class name', value='text-size-xxl-UPhmI').text.strip()
        address = driver.find_element(by='class name', value='style-item-address-KooqC').text.strip().replace('\n', ' ')
        price_metr2 = driver.find_element(by='class name', value='style-item-price-sub-price-_5RUD').text.strip()

        info_dict_apartment_house = {'url': url_link,
                                     'Застройщик': name_developer,
                                     'Цена': price,
                                     'Продавец': trader,
                                     'Цена за метр': price_metr2,
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

        driver.find_element(by='xpath', value='//button[@data-marker="item-phone-button/card"]').click()
        driver.implicitly_wait(15)

        sleep(2)
        # Добавил sleep, так как порой делает скрин ещё не прогруженной страницы.

        driver.save_screenshot(filename='/home/ivan/PycharmProjects/pythonProject/phone.png')
        x = 90
        y = 70
        w = 470
        h = 150
        # Пришлось делать скрин сразу. Но при автоопределении координат, резалось неправильно. Пришлось подгонять самому.
        # А скрин не тех размеров, и с авто координатами обрезает неверно.
        # Selenium при работе в фоновом режиме, работает в разрешении 800-600.
        fullImg = Image.open("/home/ivan/PycharmProjects/pythonProject/phone.png")
        cropImg = fullImg.crop((x, y, w, h))
        cropImg.save('/home/ivan/PycharmProjects/pythonProject/phone1.png')

        no_phone = ' '.join(Reader(['ru']).readtext('/home/ivan/PycharmProjects/pythonProject/phone1.png', detail=0))
        phone = ''
        for _ in no_phone:
            if _.isdigit():
                phone += _
        # Пришлось срезы делать с запасом, и проходить этот цикл, чтоб только цифры взять.

        info_dict_apartment_house['Телефон'] = phone
        # Надо было это сделать, на страницах разные крестики могут быть, и адреса у них разные. Схожего элемента нет.

        all_info_about_the_apartment = driver.find_elements(by='class name', value='params-paramsList__item-appQw')
        for point_info in all_info_about_the_apartment:
            lst_point = point_info.text.split(':')
            info_dict_apartment_house[lst_point[0].strip()] = lst_point[1].strip()

        all_info_the_house = driver.find_elements(by='class name', value='style-item-params-list-item-aXXql')
        for point_info in all_info_the_house:
            lst_point = point_info.text.split(':')
            info_dict_apartment_house[lst_point[0].strip()] = lst_point[1].strip()

        with open('apartments.csv', 'a') as f_csv:
            writer = csv.DictWriter(f_csv, fieldnames=info_dict_apartment_house.keys())

            if flag_write_headers:
                writer.writeheader()

            writer.writerow(info_dict_apartment_house)
    except:
        url_link = driver.current_url
        print(url_link)
        # сделал для контроля, если всё упадёт на поиске элемента, что б понять, есть этот элемент или не догрузилось.
