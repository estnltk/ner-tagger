from .defaults import *

DEBUG = False
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

ALLOWED_HOSTS = ['nertagger.ut.ee', '192.30.252.131', '127.0.0.1', 'localhost']

STATIC_ROOT = '/var/www/nertagger/static/'

DATABASES = {
    'default': dict(
        ENGINE='django.db.backends.postgresql_psycopg2',
        HOST=config.get('DB', 'host'),
        NAME=config.get('DB', 'db'),
        USER=config.get('DB', 'user'),
        PASSWORD=config.get('DB', 'password'),
        PORT=config.get('DB', 'port'),
    )
}
