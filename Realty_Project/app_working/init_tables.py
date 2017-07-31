from app import db
from app.models import Material, TypeHouse, TypeLand

def init_const_tables():
    # заполнение таблицы типов материалов стен
    db.session.add(Material(name="кирпичный"))
    db.session.add(Material(name="блочный"))
    db.session.add(Material(name="монолитный"))
    db.session.add(Material(name="панельный"))
    db.session.add(Material(name="деревянный"))
    db.session.add(Material(name="кирпич"))
    db.session.add(Material(name="пеноблоки"))
    db.session.add(Material(name="ж/б панели"))
    db.session.add(Material(name="бревно"))
    db.session.add(Material(name="металл"))
    db.session.add(Material(name="сэндвич-панели"))
    db.session.add(Material(name="брус"))
    db.session.add(Material(name="газоблоки"))
    db.session.add(Material(name="экспериментальные материалы"))

    # # заполнение таблицы типов домов
    db.session.add(TypeHouse(name="Дом"))
    db.session.add(TypeHouse(name="Дача"))
    db.session.add(TypeHouse(name="Коттедж"))
    db.session.add(TypeHouse(name="Таунхаус"))

    # заполнение таблицы типов земельных участков
    db.session.add(TypeLand(name="Сельхозназначения"))
    db.session.add(TypeLand(name="Промназначения"))
    db.session.add(TypeLand(name="Поселений"))

    db.session.commit()