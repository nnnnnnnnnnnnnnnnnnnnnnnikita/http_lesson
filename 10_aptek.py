import sys
from io import BytesIO
# Этот класс поможет нам сделать картинку из потока байт
import requests
import math
from PIL import Image
import special_func
all = []

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


for i in range(10):
    # Получаем первую найденную организацию.
    organization = json_response["features"][i]
    # Название организации.
    org_name = organization["properties"]["CompanyMetaData"]["name"]
    # Адрес организации.
    org_address = organization["properties"]["CompanyMetaData"]["address"]
    working_time = organization["properties"]["CompanyMetaData"]["Hours"]["text"]


    # Получаем координаты ответа.
    point = organization["geometry"]["coordinates"]
    org_point = "{0},{1}".format(point[0], point[1])

    if working_time == '':
        all.append("{0},pmgrm".format(org_point))
    else:
        if 'круглосуточно' in working_time:
            all.append("{0},pmgnm".format(org_point))
        else:
            all.append("{0},pmblm".format(org_point))



# Собираем параметры для запроса к StaticMapsAPI:
map_params = {
    "l": "map",
    # добавим точку, чтобы указать найденную аптеку
    "pt": "~".join(all)
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
# ... и выполняем запрос
response = requests.get(map_api_server, params=map_params)
Image.open(BytesIO(
    response.content)).show()