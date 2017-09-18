import json
import msvcrt
import os
import shutil
from random import choice
from random import uniform
from time import sleep
from config import data_path
import requests
from lxml.html import fromstring

BASE_URL='https://www.avito.ru'
LAST_PAGE='.pagination-pages.clearfix'# последняя страница
KVAR='/kvartiry'
DOMA='/doma_dachi_kottedzhi'
YCHAS='/zemelnye_uchastki'
PROD='/prodam'
OBJ_PATH='.js-catalog_after-ads .description .title.item-description-title'# путь к объету
ADRESS='.item-map.js-item-map .item-map-location'
H_MAT='.item-view-block .item-params .item-params-list'


def repSymb(s, ch_old, ch_new):#замена одного символа на другой
    s_new  = s[1:]
    i = s_new.find(ch_old)
    while i !=-1:
        s_new = s_new[0:i] + ch_new+s_new[i+1:]
        i = s_new.find(ch_old)
    return s_new


def get_all_pages(obl_url, user_agents_list=None, proxy_list=None):# получение общего числа страниц
    print('Getting total pages...')
    str_page = '' # промжуточная строка с количеством страниц
    pages = 1
    sleep(uniform(3, 6))
    f = None
    schet = len(user_agents_list) * len(proxy_list)  # защита от зацикливания
    s = 0
    while 1 and not msvcrt.kbhit() and s<schet:
        proxy = {'http': 'http://' + choice(proxy_list)}
        user_agent = {'User-Agent': choice(user_agents_list)}
        print('Try connect to server...%d' % s)
        try:
            f = requests.get(obl_url, headers=user_agent, proxies=proxy)
            if s==200:
                f = requests.get(obl_url)
            if f.status_code != 200:
                f.raise_for_status()
        except:
            s = s + 1
            continue
        else:
            break
    if not f:
        print('Not successful or 1 page in region!')
        print('Function is interrupt!')
        return pages
    print('Connect successful!')
    list_html = f.text
    list_doc = fromstring(list_html)

    for elem in list_doc.cssselect(LAST_PAGE):
        a = elem.cssselect('a')[-1]
        page_href = a.get('href')
        str_page += page_href.split('=')[1]

    if str_page.isdigit(): # на случай если страница всего одна
        pages = int(str_page)

    print('Successful! Total pages is %d!' %pages)
    return pages


def get_data_dict(url_list, user_agents_list=None, proxy_list=None):# получение словоря с первичными данными об объекте

    title = [] # заголовок
    url_s = [] # ссылка
    price = [] # цена

    for i in range(0, len(url_list)):
        pages=get_all_pages(url_list[i], user_agents_list, proxy_list)
        pages = 1
        for j in range(1, (pages+1)):
            sleep(uniform(3, 6))  # задержка
            d = None
            schet = len(user_agents_list) * len(proxy_list)# защита от зацикливания
            s = 0
            while 1 and not msvcrt.kbhit() and s<schet:
                print('Try connect to server...%d' %s)
                proxy = {'http': 'http://' + choice(proxy_list)}
                user_agent = {'User-Agent': choice(user_agents_list)}
                try:
                    d = requests.get(url_list[i] + '?p=%d' %j, headers=user_agent, proxies=proxy)
                    if s == 200:
                        d = requests.get(url_list[i] + '?p=%d' % j)
                    if d.status_code != 200:
                        d.raise_for_status()
                except:
                    s = s + 1
                    continue
                else:
                    break
            if not d:
                dict_obj = {
                    "title": title,
                    "url_s": url_s,
                    "price": price
                }
                print('Function is interrupt!')
                return dict_obj
            print('Connection successful!')
            list_html = d.text
            list_doc = fromstring(list_html)
            print('Progress>>%1.2f%%' % (((i / len(url_list)) + (j / pages / 10)) * 100))

            for elem in list_doc.cssselect(OBJ_PATH):
                a = elem.cssselect('a')
                for f in range(0, len(a)):
                    title.append(a[f].get('title'))
                    url_s.append(BASE_URL + a[f].get('href'))

            for elem in list_doc.cssselect('.js-catalog_after-ads .description .about'):
                pr = ''
                for k in range(0, len(elem.text.strip().split(' '))-1):
                    pr = pr + elem.text.strip().split(' ')[k]
                price.append(pr)
            print('Data saved in list!')

    dict_obj = {
        "title": title,
        "url_s": url_s,
        "price": price
    }
    print('Object is get!')
    return dict_obj


def form_of_kvartira(title, url_obj, price, user_agents_list=None, proxy_list=None): # заполняет форму данными(квартира)
    t_of_object = ''
    h_material = ''
    count_rooms = ''
    square = ''
    etaj = ''
    vsego_etaj = ''
    adress = ''
    id_obj = ''

    if title.find('Студия') == -1:
        count_rooms += title[title.find('-')-1]
    else:
        count_rooms += '1'

    for i in range(title.find(','), title.find('м²')):
        if title[i].isdigit():
            square = square + title[i]

    for i in range(title.rfind(','), title.find('/')):
        if title[i].isdigit():
            etaj = etaj + title[i]

    for i in range(title.find('/'), title.find('эт.')):
        if title[i].isdigit():
            vsego_etaj = vsego_etaj + title[i]

    for i in range(url_obj.rfind('_')+1, len(url_obj)):
        id_obj = id_obj + url_obj[i]

    sleep(uniform(3, 6))
    f = None
    schet = len(user_agents_list) * len(proxy_list)# защита от зацикливания
    s = 0
    while 1 and not msvcrt.kbhit() and s<schet:
        print('Try connect to server...%d' % s)
        proxy = {'http': 'http://' + choice(proxy_list)}
        user_agent = {'User-Agent': choice(user_agents_list)}
        try:
            f = requests.get(url_obj, headers=user_agent, proxies=proxy)
            if s == 200:
                f = requests.get(url_obj)
            if f.status_code == 404:
                return 0
            if f.status_code != 200:
                f.raise_for_status()
        except:
            s = s + 1
            continue
        else:
            break
    if not f:
        print('Function is interrupt!')
        return 0
    print('Connection successful!')
    list_html=f.text
    list_doc=fromstring(list_html)

    for elem in list_doc.cssselect(ADRESS):
        span = elem.cssselect('span')[1]
        try:
            span_3 = elem.cssselect('span.item-map-address')[0]
            adress = span.text + ', ' + span_3.cssselect('span')[2].text.strip()
        except:
            adress = span.text

    for elem in list_doc.cssselect(H_MAT):
        for li in elem.cssselect('li'):
            if li.cssselect('span')[0].text.find('Тип дома: ')>-1:
                if elem.cssselect('li').index(li) == 3:
                    t_of_object += 'Вторичная'
                else:
                    t_of_object += 'Новостройка'
                h_material += li.xpath('text()')[1].strip()

    obj = {
        "Type of realty": "Квартира",
        "Type of object": t_of_object,
        "House material": h_material,
        "Number of rooms": count_rooms,
        "Flat square": square,
        "Storey": etaj,
        "Number of storey": vsego_etaj,
        "Price": price,
        "Adress": adress,
        "Domain": "www.avito.ru",
        "URL": url_obj,
        "Id from site": id_obj
    }
    print('Data about object is get!')
    return obj


def form_of_dom(title, url_obj, price, user_agents_list=None, proxy_list=None): # заполняет форму данными(дом)
    t_of_object = ''
    h_material = ''
    h_square = ''
    l_square = ''
    vsego_etaj = ''
    adress = ''
    id_obj = ''

    t_of_object += title.split(' ')[0]
    h_square += title.split(' ')[1]
    l_square += title.split(' ')[5] + '00'

    for i in range(url_obj.rfind('_')+1, len(url_obj)):
        id_obj = id_obj + url_obj[i]

    sleep(uniform(3, 6))
    f = None
    schet = len(user_agents_list) * len(proxy_list)# защита от зацикливания
    s = 0
    while 1 and not msvcrt.kbhit() and s<schet:
        print('Try connect to server...%d' % s)
        proxy = {'http': 'http://' + choice(proxy_list)}
        user_agent = {'User-Agent': choice(user_agents_list)}
        try:
            f = requests.get(url_obj, headers=user_agent, proxies=proxy)
            if s == 200:
                f = requests.get(url_obj)
            if f.status_code == 404:
                return 0
            if f.status_code != 200:
                f.raise_for_status()
        except:
            s = s + 1
            continue
        else:
            break
    if not f:
        print('Function is interrupt!')
        return 0
    print('Connection successful!')
    list_html=f.text
    list_doc=fromstring(list_html)

    for elem in list_doc.cssselect(ADRESS):
        span = elem.cssselect('span')[1]
        try:
            span_3 = elem.cssselect('span.item-map-address')[0]
            adress = span.text + ', ' + span_3.cssselect('span')[2].text.strip()
        except:
            adress = span.text

    for elem in list_doc.cssselect(H_MAT):
        for li in elem.cssselect('li'):
            if li.cssselect('span')[0].text.find('Материал стен: ')>-1:
                h_material += li.xpath('text()')[1].strip()
            if li.cssselect('span')[0].text.find('Этажей в доме: ')>-1:
                vsego_etaj += li.xpath('text()')[1].strip()

    obj = {
        "Type of realty": "Дом",
        "Type of object": t_of_object,
        "House material": h_material,
        "House square": h_square,
        "Land square": l_square,
        "Number of storey": vsego_etaj,
        "Price": price,
        "Adress": adress,
        "Domain": "www.avito.ru",
        "URL": url_obj,
        "Id from site": id_obj

    }
    print('Data about object is get!')
    return obj


def form_of_ychactok(title, url_obj, price, user_agents_list=None, proxy_list=None): # заполняет форму данными(участок)
    t_of_object = ''
    square = ''
    adress = ''
    id_obj = ''

    square += title.split(' ')[1]
    t_of_object += title.split(' ')[3]

    if t_of_object == '(ИЖС)':
        t_of_object = 'Поселений'
    elif t_of_object == '(промназначения)':
        t_of_object = 'Промназначения'
    elif t_of_object == '(СНТ,':
        t_of_object = 'Сельхозназначения'

    for i in range(url_obj.rfind('_')+1, len(url_obj)):
        id_obj = id_obj + url_obj[i]

    sleep(uniform(3, 6))
    f = None
    schet = len(user_agents_list) * len(proxy_list)# защита от зацикливания
    s = 0
    while 1 and not msvcrt.kbhit() and s<schet:
        print('Try connect to server...%d' % s)
        proxy = {'http': 'http://' + choice(proxy_list)}
        user_agent = {'User-Agent': choice(user_agents_list)}
        try:
            f = requests.get(url_obj, headers=user_agent, proxies=proxy)
            if s == 200:
                f = requests.get(url_obj)
            if f.status_code == 404:
                return 0
            if f.status_code != 200:
                f.raise_for_status()
        except:
            s = s + 1
            continue
        else:
            break
    if not f:
        print('Function is interrupt!')
        return 0
    print('Connection successful!')
    list_html=f.text
    list_doc=fromstring(list_html)

    for elem in list_doc.cssselect(ADRESS):
        span = elem.cssselect('span')[1]
        try:
            span_3 = elem.cssselect('span.item-map-address')[0]
            adress = span.text + ', ' + span_3.cssselect('span')[2].text.strip()
        except:
            adress = span.text

    obj = {
        "Type of realty": "Участок",
        "Type of object": t_of_object,
        "Land square": square,
        "Price": price,
        "Adress": adress,
        "Domain": "www.avito.ru",
        "URL": url_obj,
        "Id from site": id_obj
    }
    print('Data about object is get!')
    return obj


def get_url_list_object_gruop(avito_counters):# получение ссылок на все области по типу недвижимости
    url_list_kvar = [] # список областей с продажей квартир
    url_list_dom = [] # список областей с продажей домов
    url_list_ychas = [] # список областей с продажей участков
    # словарь со списками
    url_list = {
        "url_list_kvar": url_list_kvar,
        "url_list_dom": url_list_dom,
        "url_list_ychas": url_list_ychas
    }

    #for i in range(0, len(avito_counters)):14 элемент массива Волгоградская область------------------------------------
    new_obl = ''
    for j in range(avito_counters[14]["url"].find('/'), avito_counters[14]["url"].rfind('/')-1):
        new_obl = new_obl + avito_counters[14]["url"][j]
    url_list_kvar.append(BASE_URL + new_obl + KVAR + PROD)
    url_list_dom.append(BASE_URL + new_obl + DOMA + PROD)
    url_list_ychas.append(BASE_URL + new_obl + YCHAS + PROD)

    return url_list


def write_json(ADS_NEW):
    try:
        ADS = []
        obj_mass = {"ADS": ADS}
        obj_mass = json.load(open('ads.json'))
    except:
        ADS = []
        obj_mass = {"ADS": ADS}

    obj_mass["ADS"].extend(ADS_NEW)
    filename = 'ads.json'
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(obj_mass, file, sort_keys=True, indent=2, ensure_ascii=False)# запись в файл json
    file.close()
    if not os.path.exists(data_path):
        os.mkdir(data_path)
    old_file = os.path.join(data_path, filename)
    if os.path.exists(old_file):
        os.remove(old_file)
    shutil.move(filename, data_path)

def main_of_PA():#---------------------ГЛАВНАЯ ФУНКЦИЯ-------------------------------
    # словарь со сылками на области
    print('Running...')

    avito_counters = [
                        {"name": "Москва", "cnt": 165459, "url": "\/moskva\/nedvizhimost"},
                        {"name": "Московская обл.", "cnt": 212848, "url": "\/moskovskaya_oblast\/nedvizhimost"},
                         {"name": "Санкт-Петербург", "cnt": 102108, "url": "\/sankt-peterburg\/nedvizhimost"},
                         {"name": "Ленинградская обл.", "cnt": 36664, "url": "\/leningradskaya_oblast\/nedvizhimost"},
                         {"name": "Адыгея", "cnt": 9386, "url": "\/adygeya\/nedvizhimost"},
                         {"name": "Алтайский край", "cnt": 40684, "url": "\/altayskiy_kray\/nedvizhimost"},
                         {"name": "Амурская обл.", "cnt": 12813, "url": "\/amurskaya_oblast\/nedvizhimost"},
                         {"name": "Архангельская обл.", "cnt": 12330, "url": "\/arhangelskaya_oblast\/nedvizhimost"},
                         {"name": "Астраханская обл.", "cnt": 20560, "url": "\/astrahanskaya_oblast\/nedvizhimost"},
                         {"name": "Башкортостан", "cnt": 67337, "url": "\/bashkortostan\/nedvizhimost"},
                         {"name": "Белгородская обл.", "cnt": 33170, "url": "\/belgorodskaya_oblast\/nedvizhimost"},
                         {"name": "Брянская обл.", "cnt": 18022, "url": "\/bryanskaya_oblast\/nedvizhimost"},
                         {"name": "Бурятия", "cnt": 12418, "url": "\/buryatiya\/nedvizhimost"},
                         {"name": "Владимирская обл.", "cnt": 42391, "url": "\/vladimirskaya_oblast\/nedvizhimost"},
                         {"name": "Волгоградская обл.", "cnt": 45312, "url": "\/volgogradskaya_oblast\/nedvizhimost"},
                         {"name": "Вологодская обл.", "cnt": 15855, "url": "\/vologodskaya_oblast\/nedvizhimost"},
                         {"name": "Воронежская обл.", "cnt": 46492, "url": "\/voronezhskaya_oblast\/nedvizhimost"},
                         {"name": "Дагестан", "cnt": 21171, "url": "\/dagestan\/nedvizhimost"},
                         {"name": "Еврейская АО", "cnt": 1981, "url": "\/evreyskaya_ao\/nedvizhimost"},
                         {"name": "Забайкальский край", "cnt": 13102, "url": "\/zabaykalskiy_kray\/nedvizhimost"},
                         {"name": "Ивановская обл.", "cnt": 16278, "url": "\/ivanovskaya_oblast\/nedvizhimost"},
                         {"name": "Ингушетия", "cnt": 776, "url": "\/ingushetiya\/nedvizhimost"},
                         {"name": "Иркутская обл.", "cnt": 47717, "url": "\/irkutskaya_oblast\/nedvizhimost"},
                         {"name": "Кабардино-Балкария", "cnt": 8662, "url": "\/kabardino-balkariya\/nedvizhimost"},
                         {"name": "Калининградская обл.", "cnt": 33162,"url": "\/kaliningradskaya_oblast\/nedvizhimost"},
                         {"name": "Калмыкия", "cnt": 2716, "url": "\/kalmykiya\/nedvizhimost"},
                         {"name": "Калужская обл.", "cnt": 27521, "url": "\/kaluzhskaya_oblast\/nedvizhimost"},
                         {"name": "Камчатский край", "cnt": 4899, "url": "\/kamchatskiy_kray\/nedvizhimost"},
                         {"name": "Карачаево-Черкесия", "cnt": 5764, "url": "\/karachaevo-cherkesiya\/nedvizhimost"},
                         {"name": "Карелия", "cnt": 11942, "url": "\/kareliya\/nedvizhimost"},
                         {"name": "Кемеровская обл.", "cnt": 43589, "url": "\/kemerovskaya_oblast\/nedvizhimost"},
                         {"name": "Кировская обл.", "cnt": 22592, "url": "\/kirovskaya_oblast\/nedvizhimost"},
                         {"name": "Коми", "cnt": 15464, "url": "\/komi\/nedvizhimost"},
                         {"name": "Костромская обл.", "cnt": 11174, "url": "\/kostromskaya_oblast\/nedvizhimost"},
                         {"name": "Краснодарский край", "cnt": 245441, "url": "\/krasnodarskiy_kray\/nedvizhimost"},
                         {"name": "Красноярский край", "cnt": 41320, "url": "\/krasnoyarskiy_kray\/nedvizhimost"},
                         {"name": "Крым", "cnt": 51910, "url": "\/respublika_krym\/nedvizhimost"},
                         {"name": "Курганская обл.", "cnt": 13933, "url": "\/kurganskaya_oblast\/nedvizhimost"},
                         {"name": "Курская обл.", "cnt": 18139, "url": "\/kurskaya_oblast\/nedvizhimost"},
                         {"name": "Липецкая обл.", "cnt": 21846, "url": "\/lipetskaya_oblast\/nedvizhimost"},
                         {"name": "Магаданская обл.", "cnt": 1997, "url": "\/magadanskaya_oblast\/nedvizhimost"},
                         {"name": "Марий Эл", "cnt": 11323, "url": "\/mariy_el\/nedvizhimost"},
                         {"name": "Мордовия", "cnt": 10656, "url": "\/mordoviya\/nedvizhimost"},
                         {"name": "Мурманская обл.", "cnt": 10090, "url": "\/murmanskaya_oblast\/nedvizhimost"},
                         {"name": "Ненецкий АО", "cnt": 242, "url": "\/nenetskiy_ao\/nedvizhimost"},
                         {"name": "Нижегородская обл.", "cnt": 58684, "url": "\/nizhegorodskaya_oblast\/nedvizhimost"},
                         {"name": "Новгородская обл.", "cnt": 13780, "url": "\/novgorodskaya_oblast\/nedvizhimost"},
                         {"name": "Новосибирская обл.", "cnt": 34086, "url": "\/novosibirskaya_oblast\/nedvizhimost"},
                         {"name": "Омская обл.", "cnt": 27412, "url": "\/omskaya_oblast\/nedvizhimost"},
                         {"name": "Оренбургская обл.", "cnt": 22325, "url": "\/orenburgskaya_oblast\/nedvizhimost"},
                         {"name": "Орловская обл.", "cnt": 12450, "url": "\/orlovskaya_oblast\/nedvizhimost"},
                         {"name": "Пензенская обл.", "cnt": 13164, "url": "\/penzenskaya_oblast\/nedvizhimost"},
                         {"name": "Пермский край", "cnt": 54686, "url": "\/permskiy_kray\/nedvizhimost"},
                         {"name": "Приморский край", "cnt": 3949, "url": "\/primorskiy_kray\/nedvizhimost"},
                         {"name": "Псковская обл.", "cnt": 13567, "url": "\/pskovskaya_oblast\/nedvizhimost"},
                         {"name": "Республика Алтай", "cnt": 3600, "url": "\/respublika_altay\/nedvizhimost"},
                         {"name": "Ростовская обл.", "cnt": 73982, "url": "\/rostovskaya_oblast\/nedvizhimost"},
                         {"name": "Рязанская обл.", "cnt": 23757, "url": "\/ryazanskaya_oblast\/nedvizhimost"},
                         {"name": "Самарская обл.", "cnt": 74202, "url": "\/samarskaya_oblast\/nedvizhimost"},
                         {"name": "Саратовская обл.", "cnt": 29040, "url": "\/saratovskaya_oblast\/nedvizhimost"},
                         {"name": "Сахалинская обл.", "cnt": 418, "url": "\/sahalinskaya_oblast\/nedvizhimost"},
                         {"name": "Саха (Якутия)", "cnt": 2688, "url": "\/saha_yakutiya\/nedvizhimost"},
                         {"name": "Свердловская обл.", "cnt": 57605, "url": "\/sverdlovskaya_oblast\/nedvizhimost"},
                         {"name": "Северная Осетия", "cnt": 10287, "url": "\/severnaya_osetiya\/nedvizhimost"},
                         {"name": "Смоленская обл.", "cnt": 20153, "url": "\/smolenskaya_oblast\/nedvizhimost"},
                         {"name": "Ставропольский край", "cnt": 56685, "url": "\/stavropolskiy_kray\/nedvizhimost"},
                         {"name": "Тамбовская обл.", "cnt": 14753, "url": "\/tambovskaya_oblast\/nedvizhimost"},
                         {"name": "Татарстан", "cnt": 88341, "url": "\/tatarstan\/nedvizhimost"},
                         {"name": "Тверская обл.", "cnt": 28456, "url": "\/tverskaya_oblast\/nedvizhimost"},
                         {"name": "Томская обл.", "cnt": 14405, "url": "\/tomskaya_oblast\/nedvizhimost"},
                         {"name": "Тульская обл.", "cnt": 28624, "url": "\/tulskaya_oblast\/nedvizhimost"},
                         {"name": "Тыва", "cnt": 702, "url": "\/tyva\/nedvizhimost"},
                         {"name": "Тюменская обл.", "cnt": 37090, "url": "\/tyumenskaya_oblast\/nedvizhimost"},
                         {"name": "Удмуртия", "cnt": 30885, "url": "\/udmurtiya\/nedvizhimost"},
                         {"name": "Ульяновская обл.", "cnt": 21703, "url": "\/ulyanovskaya_oblast\/nedvizhimost"},
                         {"name": "Хабаровский край", "cnt": 22275, "url": "\/habarovskiy_kray\/nedvizhimost"},
                         {"name": "Хакасия", "cnt": 10995, "url": "\/hakasiya\/nedvizhimost"},
                         {"name": "Ханты-Мансийский АО", "cnt": 35140, "url": "\/hanty-mansiyskiy_ao\/nedvizhimost"},
                         {"name": "Челябинская обл.", "cnt": 65940, "url": "\/chelyabinskaya_oblast\/nedvizhimost"},
                         {"name": "Чеченская Республика", "cnt": 5880,"url": "\/chechenskaya_respublika\/nedvizhimost"},
                         {"name": "Чувашия", "cnt": 17071, "url": "\/chuvashiya\/nedvizhimost"},
                         {"name": "Чукотский АО", "cnt": 29, "url": "\/chukotskiy_ao\/nedvizhimost"},
                         {"name": "Ямало-Ненецкий АО", "cnt": 9892, "url": "\/yamalo-nenetskiy_ao\/nedvizhimost"},
                         {"name": "Ярославская обл.", "cnt": 32767, "url": "\/yaroslavskaya_oblast\/nedvizhimost"}
                      ]

    proxy_list=[]
    files_path = os.path.abspath(os.path.dirname(__file__))
    proxy_path = os.path.join(files_path, 'proxy.txt')
    proxy_list_tab = open(proxy_path).read().split('\n')
    user_agents_path = os.path.join(files_path, 'useragents.txt')
    user_agents_list = open(user_agents_path).read().split('\n')
    for i in proxy_list_tab:
        proxy_list.append(repSymb(i, '\t', ':'))

    print('Collection of all object...')
    url_list=get_url_list_object_gruop(avito_counters)
    print('Press any key to Stop.')
    print('Collection apartments...')
    dict_kvar = get_data_dict(url_list["url_list_kvar"], user_agents_list, proxy_list)
    if msvcrt.kbhit():
        msvcrt.getch()# очистка буфера клавиатуры сброс kbhit()
    # print('Press any key to Stop.')
    # print('Collection houses...')
    dict_dom = get_data_dict(url_list["url_list_dom"], user_agents_list, proxy_list)
    if msvcrt.kbhit():
        msvcrt.getch()# очистка буфера клавиатуры сброс kbhit()
    # print('Press any key to Stop.')
    # print('Collection Land plots...')
    dict_ychas = get_data_dict(url_list["url_list_ychas"], user_agents_list, proxy_list)
    if msvcrt.kbhit():
        msvcrt.getch()# очистка буфера клавиатуры сброс kbhit()
    # print('Collection is finished.')

    ADS = [] #список с объектами

    print('Parsing... Press any key to Stop.')
    for i in range(0, len(dict_kvar["title"])):
        obj = form_of_kvartira(dict_kvar["title"][i], dict_kvar["url_s"][i], dict_kvar["price"][i], user_agents_list, proxy_list)
        if obj:
            ADS.append(obj)
        print('Progress 1/3 >>%1.2f%%' % (i / len(dict_kvar["title"]) * 100))
        if msvcrt.kbhit():
            break

    for i in range(0, len(dict_dom["title"])):
        obj = form_of_dom(dict_dom["title"][i], dict_dom["url_s"][i], dict_dom["price"][i], user_agents_list, proxy_list)
        if obj:
            ADS.append(obj)
        print('Progress 2/3 >>%1.2f%%' % (i / len(dict_dom["title"]) * 100))
        if msvcrt.kbhit():
            break

    for i in range(0, len(dict_ychas["title"])):
        obj = form_of_ychactok(dict_ychas["title"][i], dict_ychas["url_s"][i], dict_ychas["price"][i], user_agents_list, proxy_list)
        if obj:
            ADS.append(obj)
        print('Progress 3/3 >>%1.2f%%' % (i / len(dict_ychas["title"]) * 100))
        if msvcrt.kbhit():
            break

    print('Parsing is finished.')

    print('Writing json fail...')
    write_json(ADS)
    print('Writing complete.')