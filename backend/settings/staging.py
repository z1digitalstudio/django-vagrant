from .common import *  # pyflakes:ignore # noqa

DATABASES['default'].update({
    'NAME': '',
    'USER': '',
    'ENGINE': 'django.db.backends.postgresql',
    'PASSWORD': '',
    'HOST': '',
    'PORT': '',
})

ALLOWED_HOSTS = []
INTERNAL_IPS = ()

STATIC_ROOT = os.path.join(BASE_DIR, '../static_root')

# Try to import local settings, if exists
try:
    EXTRA_APPS = ()
    from local import *  # pyflakes:ignore # noqa
    if EXTRA_APPS:
        INSTALLED_APPS = INSTALLED_APPS + EXTRA_APPS
except ImportError:
    pass
