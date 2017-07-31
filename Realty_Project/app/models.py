from app import db

metadata = db.MetaData()
#=========================================================================================================
#таблица, описывающая сущность КВАРТИРА
class Flat(db.Model):
    # query = db.session.query_property()
    __tablename__ = 'flat'

    id = db.Column(db.Integer, primary_key=True)  # идентификатор записи в таблице
    idTypeFlat = db.Column(db.SmallInteger, nullable=False)  # тип квартиры (вторичная/новостройка)
    idMaterial = db.Column(db.Integer, db.ForeignKey('material.id'))  # идентификатор типа материала дома, в котором располагается квартира
    flatSquare = db.Column(db.Float, nullable=False)  # площадь квартиры
    roomCount = db.Column(db.Integer, nullable=False)  # число комнат в квартире
    numFloor = db.Column(db.Integer, nullable=False)  # номер этаж квартиры
    countFloor = db.Column(db.Integer, nullable=False)  # число этажей в доме
    price = db.Column(db.Integer, nullable=False)  # цена квартиры
    address = db.Column(db.String(200), nullable=False)  # адрес дома
    domain = db.Column(db.String(140), nullable=False)  # домен сайта-источника
    url = db.Column(db.String(300), nullable=False)  # прямая ссылка на объявление
    idAdSite = db.Column(db.Integer, nullable=False)  # идентификатор объявления на сайте
    dateAddToDB = db.Column(db.Date, nullable=False)  # дата добавления записи в базу данных проекта
    idDataMap = db.Column(db.Integer, db.ForeignKey('datamap.id'))  # идентификатор записи в таблице координат для объекта
    isTopicality = db.Column(db.Integer, nullable=False) # актуальность записи на данный момент

    # метод, представляющий вывод данных класса
    def __repr__(self):
        return '<Flat %r> ' % (self.id) % '; ' % (self.idTypeFlat) % \
                '; ' % (self.idMaterial) % '; ' % (self.flatSquare) % \
                '; ' % (self.roomCount) % '; ' % (self.numFloor) % '; ' \
                % (self.countFloor) % '; ' % (self.price) % '; ' % (self.address) \
                % '; ' % (self.domain) % '; ' % (self.url) % '; ' % (self.idAdSite) \
                % '; ' % (self.dateAddToDB) % '; ' % (self.idDataMap) % '; ' % (self.isTopicality)

# =========================================================================================================
# таблица, описывающая сущность ДОМ
class House(db.Model):
    __tablename__ = 'house'
    id = db.Column(db.Integer, primary_key=True)  # идентификатор записи в таблице
    idTypeHouse = db.Column(db.Integer, db.ForeignKey('typehouse.id'))  # тип дома (дом/дача/коттедж/таунхаус)
    idMaterial = db.Column(db.Integer, db.ForeignKey('material.id'))  # идентификатор типа материала дома
    houseSquare = db.Column(db.Float, nullable=False)  # площадь дома
    landSquare = db.Column(db.Float, nullable=False)  # площадь прилегающего земельного участка
    countFloor = db.Column(db.Integer, nullable=False)  # число этажей в доме
    price = db.Column(db.Integer, nullable=False)  # цена объекта
    address = db.Column(db.String(200), nullable=False)  # адрес дома
    domain = db.Column(db.String(140), nullable=False)  # домен сайта-источника
    url = db.Column(db.String(300), nullable=False)  # прямая ссылка на объявление
    idAdSite = db.Column(db.Integer, nullable=False)  # идентификатор объявления на сайте
    dateAddToDB = db.Column(db.Date, nullable=False)  # дата добавления записи в базу данных проекта
    idDataMap = db.Column(db.Integer, db.ForeignKey('datamap.id'))  # идентификатор записи в таблице координат для объекта
    isTopicality = db.Column(db.Integer, nullable=False)  # актуальность записи на данный момент

    # метод, представляющий вывод данных класса
    def __repr__(self):
        return '<House %r> ' % (self.id) % '; ' % (self.idTypeHouse) % \
                '; ' % (self.idMaterial) % '; ' % (self.houseSquare) % \
                '; ' % (self.landSquare) % '; '  % (self.countFloor) % \
               '; ' % (self.price) % '; ' % (self.address) % '; ' % (self.domain) % \
               '; ' % (self.url) % '; ' % (self.idAdSite) % '; ' % (self.dateAddToDB) % \
               '; ' % (self.idDataMap) % '; ' % (self.isTopicality)

# =========================================================================================================
# таблица, описывающая сущность ДОМ
class Land(db.Model):
    __tablename__ = 'land'
    id = db.Column(db.Integer, primary_key=True)  # идентификатор записи в таблице
    idTypeLand = db.Column(db.Integer, db.ForeignKey('typeland.id'))  # тип земельного участка
    landSquare = db.Column(db.Float, nullable=False)  # площадь земельного участка
    price = db.Column(db.Integer, nullable=False)  # цена объекта
    address = db.Column(db.String(200), nullable=False)  # адрес земельного участка
    domain = db.Column(db.String(140), nullable=False)  # домен сайта-источника
    url = db.Column(db.String(300), nullable=False)  # прямая ссылка на объявление
    idAdSite = db.Column(db.Integer, nullable=False)  # идентификатор объявления на сайте
    dateAddToDB = db.Column(db.Date, nullable=False)  # дата добавления записи в базу данных проекта
    idDataMap = db.Column(db.Integer, db.ForeignKey('datamap.id'))  # идентификатор записи в таблице координат для объекта
    isTopicality = db.Column(db.Integer, nullable=False)  # актуальность записи на данный момент

    # метод, представляющий вывод данных класса
    def __repr__(self):
        return '<Land %r> ' % (self.id) % '; ' % (self.idTypeLand) % \
                '; ' % (self.landSquare)% '; ' % (self.price) % '; ' % \
               (self.address) % '; ' % (self.domain) % '; ' % (self.url) % \
               '; ' % (self.idAdSite) % '; ' % (self.dateAddToDB) % \
                '; ' % (self.idDataMap) % '; ' % (self.isTopicality)

# =========================================================================================================
# таблица, описывающая сущность ТИПЫ ЧАСТНЫХ ДОМОВ
class TypeHouse(db.Model):
    __tablename__ = 'typehouse'
    id = db.Column(db.Integer, primary_key=True)  # идентификатор записи в таблице
    name = db.Column(db.String, nullable=False)  # название типа частных домов
    houseTypeRelationship = db.relationship('House', backref="typeHouses")
    # метод, представляющий вывод данных класса
    def __repr__(self):
        return '<TypeHouse %r> ' % (self.id) % '; ' % (self.name)

# =========================================================================================================
# таблица, описывающая сущность ТИПЫ ЗЕМЕЛЬНЫХ УЧАСТКОВ
class TypeLand(db.Model):
    __tablename__ = 'typeland'
    id = db.Column(db.Integer, primary_key=True)  # идентификатор записи в таблице
    name = db.Column(db.String, nullable=False)  # название типа земельных участков

    landTypeRelationship = db.relationship('Land', backref="typeLands")

    # метод, представляющий вывод данных класса
    def __repr__(self):
        return '<TypeLand %r> ' % (self.id) % '; ' % (self.name)

#=========================================================================================================
#таблица, описывающая сущность МАТЕРИАЛЫ СТЕН
class Material(db.Model):
    __tablename__ = 'material'
    # query = db.session.query_property()
    id = db.Column(db.Integer, primary_key=True)  # идентификатор записи в таблице
    name = db.Column(db.String, nullable=False)  # название материала

    flatMaterialRelationship = db.relationship('Flat', backref="material")
    houseMaterialRelationship = db.relationship('House', backref="material")

    # метод, представляющий вывод данных класса
    def __repr__(self):
        return '<Material %r> ' % (self.id) % '; ' % (self.name)

#=========================================================================================================
#таблица, описывающая сущность ДАННЫЕ ДЛЯ КАРТЫ
class DataMap(db.Model):
    __tablename__ = 'datamap'
    id = db.Column(db.Integer, primary_key=True)  # идентификатор записи в таблице
    latitude = db.Column(db.String(10), nullable=False)#широта
    longitude = db.Column(db.String(10), nullable=False)#долгота

    flatDataMap = db.relationship("Flat", backref="dataMapOfFlat")
    houseDataMap = db.relationship("House", backref="dataMapOfHouse")
    landDataMap = db.relationship("Land", backref="dataMapOfLand")

    # метод, представляющий вывод данных класса
    def __repr__(self):
        return '<DataMAP %r> ' % (self.id) % '; ' % (self.latitude)\
               % '; ' % (self.longitude)