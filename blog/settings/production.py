from .base import *

DEBUG=False

DATABASES = {
     'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'webmash_prod',
        'USER': 'u_webmash',
        'PASSWORD': 'Gagan@9891095633@2000',
        'HOST': 'localhost',
        'PORT': '',
    }
}

ALLOWED_HOSTS = ['192.168.43.86','127.0.0.1','157.245.108.160','webmash.saporasignal.me','www.webmash.saporasocial.me','.webmash.saporasocial.me']