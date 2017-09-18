from app import db
from app.models import Dictionary

def init_const_tables():
    # заполнение таблицы типов материалов стен
    db.session.add(Dictionary(name="кирпичный"))
    db.session.add(Dictionary(name="блочный"))
    db.session.add(Dictionary(name="монолитный"))
    db.session.add(Dictionary(name="панельный"))
    db.session.add(Dictionary(name="деревянный"))
    db.session.add(Dictionary(name="кирпич"))
    db.session.add(Dictionary(name="пеноблоки"))
    db.session.add(Dictionary(name="ж/б панели"))
    db.session.add(Dictionary(name="бревно"))
    db.session.add(Dictionary(name="металл"))
    db.session.add(Dictionary(name="сэндвич-панели"))
    db.session.add(Dictionary(name="брус"))
    db.session.add(Dictionary(name="газоблоки"))
    db.session.add(Dictionary(name="экспериментальные материалы"))
    # заполнение таблицы типов домов
    db.session.add(Dictionary(name="Дом"))
    db.session.add(Dictionary(name="Дача"))
    db.session.add(Dictionary(name="Коттедж"))
    db.session.add(Dictionary(name="Таунхаус"))
    # заполнение таблицы типов земельных участков
    db.session.add(Dictionary(name="Сельхозназначения"))
    db.session.add(Dictionary(name="Промназначения"))
    db.session.add(Dictionary(name="Поселений"))

    db.session.commit()