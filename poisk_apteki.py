import sys
from io import BytesIO
import math
# Этот класс поможет нам сделать картинку из потока байт
import requests
from PIL import Image
import special_func
import pygame.freetype  # Import the freetype module.


def distance(ra, rb):
    rst = 111 * 1000
    ra1, ra2 = ra
    rb1, rb2 = rb

    radians_lattitude = math.radians((ra2 + rb2) / 2.)
    lat_lon_factor = math.cos(radians_lattitude)
    x3 = abs(ra1 - rb1) * rst * lat_lon_factor
    y3 = abs(ra2 - rb2) * rst
    dist = math.sqrt(x3 * x3 + y3 * y3)

    return dist


# Пусть наше приложение предполагает запуск:
# python search.py Москва, ул. Ак. Королева, 12
# Тогда запрос к геокодеру формируется следующим образом:
toponym_to_find = " ".join(sys.argv[1:])

api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)
if not response:
    # обработка ошибочной ситуации
    pass

r = response.json()
x1, y1 = special_func.func(r)


# Преобразуем ответ в json-объект
json_response = response.json()
# Получаем первый топоним из ответа геокодера.
toponym = json_response["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]
# Координаты центра топонима:
toponym_coodrinates = toponym["Point"]["pos"]
# Долгота и широта:
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

search_api_server = "https://search-maps.yandex.ru/v1/"



search_params = {
    "apikey": api_key,
    "text": "аптека",
    "lang": "ru_RU",
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "type": "biz"
}

response = requests.get(search_api_server, params=search_params)



if not response:
    #...
    pass

# Преобразуем ответ в json-объект
json_response = response.json()

# Получаем первую найденную организацию.
organization = json_response["features"][0]
# Название организации.
org_name = organization["properties"]["CompanyMetaData"]["name"]
# Адрес организации.
org_address = organization["properties"]["CompanyMetaData"]["address"]
wt = organization["properties"]["CompanyMetaData"]["Hours"]["text"]

# Получаем координаты ответа.
point = organization["geometry"]["coordinates"]
org_point = "{0},{1}".format(point[0], point[1])

# Собираем параметры для запроса к StaticMapsAPI:
map_params = {
    "l": "map",
    # добавим точку, чтобы указать найденную аптеку
    "pt": "~".join(["{0},pma".format(org_point), "{0},pmb".format(f'{toponym_longitude},{toponym_lattitude}')])
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
# ... и выполняем запрос
response = requests.get(map_api_server, params=map_params)

Image.open(BytesIO(
    response.content)).show()
# Создадим картинку
# и тут же ее покажем встроенным просмотрщиком операционной системы

dis = distance((float(point[0]), float(point[1])), (float(toponym_longitude), float(toponym_lattitude)))

pygame.init()
screen = pygame.display.set_mode((800, 600))
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    text_lines = ["ВЫВОД:", "",
                  f'АДРЕС: {org_address}',
                  f'НАЗВАНИЕ: {org_name}',
                  f'ВРЕМЯ РАБОТЫ: {wt}',
                  f'ДИСТАНЦИЯ: {dis}']


    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 30)
    t = 50
    for line in text_lines:
        sr = font.render(line, 1, pygame.Color('white'))
        tl = sr.get_rect()
        t += 10
        tl.top = t
        tl.x = 10
        t += tl.height
        screen.blit(sr, tl)

    pygame.display.flip()

pygame.quit()