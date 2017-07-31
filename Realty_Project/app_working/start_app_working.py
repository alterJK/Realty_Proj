from app import db
from app.models import Material
from app_working.init_tables import init_const_tables
from app_working.parser_working.parser_avito import main_of_PA
from app_working.process_data.make_common_data_json import make_json_data
from app_working.save_data_to_DB import readDataFromJSON
from app_working.preporation_tables import start_preporation_tables, finish_preporation_tables

def start_work_with_data():
    # проверка заполнения константных таблиц
    if db.session.query(Material).count() == 0:
        init_const_tables()
    # заполнение промежуточных значений актуальности объявлений
    start_preporation_tables()
    # включение парсера
    main_of_PA()
    # формирование json-файла для записи в базу данных
    make_json_data()
    # запись в базу данных
    readDataFromJSON()
    # завершение обработки значений актуальности
    finish_preporation_tables()