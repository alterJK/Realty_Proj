import codecs
import json
import os

from app.models import*
from datetime import *

from app_working.check_record_in_DB import check_coordinates_in_DB, check_flats_in_DB, \
                                            check_houses_in_DB, check_lands_in_DB


currentDate = datetime.now().date()

def save_flat_to_DB(obj):
    idMapData = check_coordinates_in_DB(obj['longitude'], obj['latitude'])
    flat = Flat()
    flat.idTypeFlat = obj['idTypeFlat']
    flat.idMaterial = obj['idMaterial']
    flat.flatSquare = obj['flatSquare']
    flat.roomCount = obj['roomCount']
    flat.numFloor = obj['numFloor']
    flat.countFloor = obj['countFloor']
    flat.price = obj['price']
    flat.address = obj['address']
    flat.domain = obj['domain']
    flat.url = obj['url']
    flat.idAdSite = obj['idAdSite']
    flat.dateAddToDB = currentDate
    flat.idDataMap = idMapData
    flat.isTopicality = 1
    check_flats_in_DB(flat)

def save_house_to_DB(obj):
    idMapData = check_coordinates_in_DB(obj['longitude'], obj['latitude'])
    house = House()
    house.idTypeHouse = obj['idTypeHouse']
    house.idMaterial = obj['idMaterial']
    house.houseSquare = obj['houseSquare']
    house.landSquare = obj['landSquare']
    house.countFloor = obj['numFloor']
    house.price = obj['price']
    house.address = obj['address']
    house.domain = obj['domain']
    house.url = obj['url']
    house.idAdSite = obj['idAdSite']
    house.dateAddToDB = currentDate
    house.idDataMap = idMapData
    house.isTopicality = 1
    check_houses_in_DB(house)

def save_land_to_DB(obj):
    idMapData = check_coordinates_in_DB(obj['longitude'], obj['latitude'])
    land = Land()
    land.idTypeLand = obj['idTypeLand']
    land.landSquare = obj['landSquare']
    land.price = obj['price']
    land.address = obj['address']
    land.domain = obj['domain']
    land.url = obj['url']
    land.idAdSite = obj['idAdSite']
    land.dateAddToDB = currentDate
    land.idDataMap = idMapData
    land.isTopicality = 1
    check_lands_in_DB(land)

def readDataFromJSON():
    # устанавливаем путь к файлу списка объявлений
    basedir = os.path.abspath(os.path.dirname(__file__))
    basedir = basedir.replace('app_working', 'process_data')
    ads_path = os.path.join(basedir, 'AdsForDB.json')
    try:
        dataJson = codecs.open(ads_path, 'r', 'utf-8')
    except IOError as e:
        print(u'Нет списка объявления для добавления в базу данных')
    else:
        with dataJson:
            d = json.load(dataJson)
            for i in d['Processed realty objects']:
                temp = str(i['typeRealty'])
                # определение id типа недвижимости
                if temp == 'Flat':
                    save_flat_to_DB(i)
                elif temp == 'House':
                    save_house_to_DB(i)
                elif temp == 'Land':
                    save_land_to_DB(i)
        dataJson.close()