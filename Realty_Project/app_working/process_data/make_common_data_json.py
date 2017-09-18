import codecs
import json
import os
import shutil

from app_working.process_data.get_coordinates import get_coordinates
from config import data_path
from app import db
from app.models import Dictionary

commonArray = []
processedObj = {'Processed realty objects': []}

#поиск id записи по содержимому
def findId(temp):
    idFinder = Dictionary.query.filter_by(name=temp)
    result = db.session.execute(idFinder)
    row = result.fetchone()
    return row[0]

def finder_coordinates_flat(obj):
    address = obj['Adress']
    objCoordinates = get_coordinates(address)

    if (objCoordinates.longAddress !=""):
        address = objCoordinates.longAddress
        if obj['Type of object'] == "Новостройка":
            typeObject = 1
        else:
            typeObject = 2
        # определение материала дома
        houseMaterial = findId(obj['House material'])
        # определение числа комнат
        numRooms = obj['Number of rooms']
        numRooms = int(numRooms)
        # определение площади квартиры
        flatSquare = obj['Flat square']
        flatSquare = float(int(flatSquare))
        # определение этажа квартиры
        storey = obj["Storey"]
        storey = int(storey)
        # определение этажности дома
        numStorey = obj['Number of storey']
        numStorey = int(numStorey)
        # определение цены объекта
        price = obj['Price']
        if (price == ""):
            price = 0
        else:
            price = int(price)
        # определение домена сайта
        domain = obj['Domain']
        # определение ссылки на объект
        url = obj['URL']
        # определение id с сайта
        idSite = obj['Id from site']
        idSite = int(idSite)

        longitude = objCoordinates.longitude
        latitude = objCoordinates.latitude

        obj = {
               'typeRealty': 'Flat',
               'idTypeFlat': typeObject,
               'idMaterial': houseMaterial,
               'flatSquare': flatSquare,
               'roomCount': numRooms,
               'numFloor': numStorey,
               'countFloor': storey,
               'price': price,
               'address': address,
               'domain': domain,
               'url': url,
               'idAdSite': idSite,
               'longitude': longitude,
               'latitude': latitude
               }
        commonArray.append(obj)


def finder_coordinates_house(obj):
    address = obj['Adress']
    objCoordinates = get_coordinates(address)

    if (objCoordinates.longAddress != ""):
        address = objCoordinates.longAddress
        typeObject = findId(obj['Type of object'])
        # определение материала дома
        houseMaterial = findId(obj['House material'])
        # определение площади дома
        houseSquare = obj['House square']
        # определение площади участка
        landSquare = obj['Land square']
        # определение этажности дома
        numStorey = obj['Number of storey']
        # определение цены объекта
        price = obj['Price']
        if (price == ""):
            price = 0
        else:
            price = int(price)
        # определение домена сайта
        domain = obj['Domain']
        # определение ссылки на объект
        url = obj['URL']
        # определение id с сайта
        idSite = obj['Id from site']
        idSite = int(idSite)

        longitude = objCoordinates.longitude
        latitude = objCoordinates.latitude

        obj = {
            'typeRealty': 'House',
            'idTypeHouse': typeObject,
            'idMaterial': houseMaterial,
            'houseSquare': houseSquare,
            'landSquare': landSquare,
            'numFloor': numStorey,
            'price': price,
            'address': address,
            'domain': domain,
            'url': url,
            'idAdSite': idSite,
            'longitude': longitude,
            'latitude': latitude
        }
        commonArray.append(obj)

def finder_coordinates_land(obj):
    address = obj['Adress']
    objCoordinates = get_coordinates(address)

    if (objCoordinates.longAddress != ""):
        address = objCoordinates.longAddress
        typeObject = findId(obj['Type of object'])
        # определение площади участка
        landSquare = obj['Land square']
        # определение цены объекта
        price = obj['Price']
        if (price == ""):
            price = 0
        else:
            price = int(price)
        # определение домена сайта
        domain = obj['Domain']
        # определение ссылки на объект
        url = obj['URL']
        # определение id с сайта
        idSite = obj['Id from site']
        idSite = int(idSite)

        longitude = objCoordinates.longitude
        latitude = objCoordinates.latitude

        obj = {
            'typeRealty': 'Land',
            'idTypeLand': typeObject,
            'landSquare': landSquare,
            'price': price,
            'address': address,
            'domain': domain,
            'url': url,
            'idAdSite': idSite,
            'longitude': longitude,
            'latitude': latitude
        }
        commonArray.append(obj)

def make_json_data():
    # устанавливаем путь к файлу списка объявлений
    file_path = os.path.join(data_path, 'ads.json')
    try:
        dataJson = codecs.open(file_path, 'r', 'utf-8')
    except IOError as e:
        print(u'Нет списка объявления для добавления в базу данных')
    else:
        with dataJson:
            d = json.load(dataJson)
            for i in d['ADS']:
                temp = str(i['Type of realty'])
                # определение id типа недвижимости
                if temp == 'Квартира':
                    finder_coordinates_flat(i)
                elif temp == 'Дом':
                    finder_coordinates_house(i)
                elif temp == 'Участок':
                    finder_coordinates_land(i)
        dataJson.close()
        processedObj['Processed realty objects'].extend(commonArray)
        filename = 'ads_for_db.json'
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(processedObj, file, sort_keys=True, indent=2, ensure_ascii=False)  # запись в файл json
        file.close()
        old_file = os.path.join(data_path, filename)
        if os.path.exists(old_file):
            os.remove(old_file)
        shutil.move(filename, data_path)