import os

DEBUG = 'RENDER' not in os.environ
postgres = os.environ.get('USE_POSTGRES')

if DEBUG:
    if postgres:
        DB_URL = 'postgresql+psycopg2://postgres:postgres@localhost:5432/faq'
    else:
        DB_URL = 'sqlite:///database.db'

else:
    DB_URL = os.environ.get('DB_URL')
    