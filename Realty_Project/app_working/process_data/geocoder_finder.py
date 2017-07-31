from geopy.geocoders import Yandex

def finder_geocode(address):
    geolocator = Yandex()
    latitude = ""
    longitude = ""
    try:
        location = geolocator.geocode(address, timeout=10)
    except:
        address = ""
        latitude = ""
        longitude = ""
        return address, latitude, longitude
    if (location == None or location.address == None):
        address = ""

    else:
        address = location._raw['metaDataProperty']['GeocoderMetaData']['text']
        latitude = location.latitude
        longitude = location.longitude

    return (address, latitude, longitude)