from .base import BASE_DIR


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dbpmname',
        'USER': 'adminUsr',
        'PASSWORD': 'postgres1',
        'HOST': '127.0.0.1',
        'PORT': '6222',
    }
}
