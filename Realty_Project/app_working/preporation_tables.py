from app.models import Flat, House, Land
from app import db

def set_topicality_before_update(table):
    # обновление уже существующих записей
    table.query.filter_by().update(dict(isTopicality=2))
    db.session.commit()

def set_untopicality_after_update(table):
    # обновление уже существующих записей
    table.query.filter_by(isTopicality = 2).update(dict(isTopicality=0))
    db.session.commit()

def start_preporation_tables():
    # подготовка таблицы FLAT
    if db.session.query(Flat).count() > 0:
        set_topicality_before_update(Flat)
    # подготовка таблицы HOUSE
    if db.session.query(House).count() > 0:
        set_topicality_before_update(House)
    # подготовка таблицы LAND
    if db.session.query(Land).count() > 0:
        set_topicality_before_update(Land)

def finish_preporation_tables():
    # подготовка таблицы FLAT
    if db.session.query(Flat).count() > 0:
        set_untopicality_after_update(Flat)
    # подготовка таблицы HOUSE
    if db.session.query(House).count() > 0:
        set_untopicality_after_update(House)
    # подготовка таблицы LAND
    if db.session.query(Land).count() > 0:
        set_untopicality_after_update(Land)