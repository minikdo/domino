from .base import BASE_DIR, ALLOWED_HOSTS, os, get_secret

DEBUG = False

ALLOWED_HOSTS += ['10.4.0.1', 'domino.d']

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

SERVER_EMAIL = get_secret('SERVER_EMAIL')
DEFAULT_FROM_EMAIL = SERVER_EMAIL
SERVER_EMAIL = SERVER_EMAIL

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': '/var/log/django/domino/request.log'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'INFO'
        }
    }
}
