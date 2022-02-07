from .base import *
ALLOWED_HOSTS = ['52.78.145.43', 'melodyboard.shop']
STATIC_ROOT = BASE_DIR / 'static/'
STATICFILES_DIRS = []
DEBUG=False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pybo',
        'USER': 'postgres',
        'PASSWORD': '=eKmx$xxymnxxwNCxxx$SX55*RdjKK1G&',
        'HOST': 'database-2.capxttw9wm6f.ap-northeast-2.rds.amazonaws.com',
        'PORT': '5432',
    }
}