from .base import BASE_DIR


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'NexusPMDB',
        'USER': 'adminUsr',
        'PASSWORD': 'postgres1',
        'HOST': 'db',
        'PORT': '5432',
    }
}
