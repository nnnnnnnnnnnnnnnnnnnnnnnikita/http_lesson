def func(response):
    res = response
    x, y = res['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['boundedBy']['Envelope'][
        'lowerCorner'].split()
    x1, y1 = res['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['boundedBy']['Envelope'][
        'upperCorner'].split()
    if float(y) >= float(y1):
        y2 = float(y) - float(y1)
    else:
        y2 = float(y1) - float(y)
    if float(x) >= float(x1):
        x2 = float(x) - float(x1)
    else:
        x2 = float(x1) - float(x)
    return (x2, y2)