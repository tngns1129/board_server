from .base import *

ALLOWED_HOSTS = ['3.37.58.70']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db',
        'USER': 'semo',
        'PASSWORD': '1234',
        'HOST': 'db',
        'PORT': '3306',
    }
}