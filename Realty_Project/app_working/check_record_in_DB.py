from app import db
from app.models import Flat, House, Land, DataMap

def check_coordinates_in_DB(longitudeObj, latitudeObj):
    findDataMap = DataMap.query.filter_by(longitude=longitudeObj, latitude=latitudeObj)
    result = db.session.execute(findDataMap)
    row=result.fetchone()
    if row == None:
        db.session.add(DataMap(longitude=longitudeObj, latitude=latitudeObj))
        return db.session.query(DataMap).count()
    else:
        return row[0]

def check_flats_in_DB(flat):
    # поиск записи в базе данных
    findFlat = Flat.query.filter_by(idTypeFlat = flat.idTypeFlat,
                                    idMaterial = flat.idMaterial,
                                    flatSquare = flat.flatSquare,
                                    roomCount  = flat.roomCount,
                                    numFloor   = flat.numFloor,
                                    countFloor = flat.countFloor,
                                    price      = flat.price,
                                    address    = flat.address,
                                    domain     = flat.domain,
                                    url        = flat.url,
                                    idAdSite   = flat.idAdSite,)
    result = db.session.execute(findFlat)
    for row in result:
        if row[7] == flat.price:
            # запись есть в БД
            # обновление уже существующих записей
            Flat.query.filter_by(id = row[0]).update(dict(isTopicality=1))
            db.session.commit()
            return
        else:
            # запись есть в БД, но значение цены другое
            db.session.add(flat)
            db.session.commit()
            # обновление уже существующих записей
            Flat.query.filter_by(id = row[0]).update(dict(isTopicality=0))
            db.session.commit()
            return
    # записи еще нет в БД
    db.session.add(flat)
    db.session.commit()

def check_houses_in_DB(house):
    # поиск записи в базе данных
    findHouse = House.query.filter_by(idTypeHouse = house.idTypeHouse,
                                      idMaterial  = house.idMaterial,
                                      houseSquare = house.houseSquare,
                                      landSquare  = house.landSquare,
                                      countFloor  = house.countFloor,
                                      price       = house.price,
                                      address     = house.address,
                                      domain      = house.domain,
                                      url         = house.url,
                                      idAdSite    = house.idAdSite,)
    result = db.session.execute(findHouse)
    for row in result:
        if row[6] == house.price:
            # запись есть в БД
            # обновление уже существующих записей
            House.query.filter_by(id = row[0]).update(dict(isTopicality=1))
            db.session.commit()
            return
        else:
            # запись есть в БД, но значение цены другое
            db.session.add(house)
            db.session.commit()
            # обновление уже существующих записей
            House.query.filter_by(id = row[0]).update(dict(isTopicality=0))
            db.session.commit()
            return
    # записи еще нет в БД
    db.session.add(house)
    db.session.commit()

def check_lands_in_DB(land):
    # поиск записи в базе данных
    findLand = Land.query.filter_by(idTypeLand  = land.idTypeLand,
                                    landSquare  = land.landSquare,
                                    price       = land.price,
                                    address     = land.address,
                                    domain      = land.domain,
                                    url         = land.url,
                                    idAdSite    = land.idAdSite,)
    result = db.session.execute(findLand)
    for row in result:
        if row[3] == land.price:
            # запись есть в БД
            # обновление уже существующих записей
            Land.query.filter_by(id = row[0]).update(dict(isTopicality=1))
            db.session.commit()
            return
        else:
            # запись есть в БД, но значение цены другое
            db.session.add(land)
            db.session.commit()
            # обновление уже существующих записей
            Land.query.filter_by(id = row[0]).update(dict(isTopicality=0))
            db.session.commit()
            return
    # записи еще нет в БД
    db.session.add(land)
    db.session.commit()