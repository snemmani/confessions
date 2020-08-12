from .jawsdb import JawsDBConnection
from .settings import *

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
jawsDb = JawsDBConnection()
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'USER': jawsDb.username,
        'PASSWORD': jawsDb.password,
        'HOST': jawsDb.host,
        'PORT': jawsDb.port,
        'NAME': jawsDb.database
    }
}
