from .base import * # noqa

DEBUG = True

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#    }
#}

INSTALLED_APPS += ['debug_toolbar', 'django_extensions']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']

INTERNAL_IPS = ['127.0.0.1', '192.168.8.101']

ALLOWED_HOSTS += ['192.168.8.101']

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  # add STATIC_ROOT to DIRS
]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
# EMAIL_FILE_PATH = os.path.join(BASE_DIR, "sent_emails)"
