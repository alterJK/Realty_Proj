import os
basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = 'realty-service-for-monitoring'

db_path = os.path.join(basedir, 'database')

if not os.path.exists(db_path):
    os.mkdir(db_path)
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(db_path, 'RealtyDB.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(db_path, 'db_repository')

data_path = os.path.join(basedir, 'data')