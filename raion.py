import sys
# Этот класс поможет нам сделать картинку из потока байт
import requests
import special_func


# Пусть наше приложение предполагает запуск:
# python search.py Москва, ул. Ак. Королева, 12
# Тогда запрос к геокодеру формируется следующим образом:
toponym_to_find = " ".join(sys.argv[1:])

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

search_api_server = "http://geocode-maps.yandex.ru/1.x/"

search_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": ",".join([toponym_longitude, toponym_lattitude]),
    'kind': 'district',
    'results': '1',
    'format': 'json'
}

response = requests.get(search_api_server, params=search_params)
print(response.json()["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]['name'])