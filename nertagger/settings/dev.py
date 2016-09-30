from .defaults import *

DEBUG = True
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

MIDDLEWARE_CLASSES.append('debug_panel.middleware.DebugPanelMiddleware')

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

