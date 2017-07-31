from app_working.process_data.geocoder_finder import finder_geocode

class MapData:
    # инициализация основных переменных геообъекта
    def init_mapData(self, longitude, latitude, longAddress):
        self.longitude = longitude
        self.latitude = latitude
        self.longAddress = longAddress

    def find_address(self):
        self.longAddress, self.latitude, self.longitude = finder_geocode(self.longAddress)

#определение координат объекта
def get_coordinates(address):
    #определение координат объекта
    longitude = ''
    latitude = ''
    objectMapData = MapData()
    objectMapData.init_mapData(longitude, latitude, address)
    if (address != ""):
        objectMapData.find_address()
    return (objectMapData)