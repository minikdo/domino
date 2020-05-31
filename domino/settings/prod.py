from .base import *  # noqa

DEBUG = False

ALLOWED_HOSTS += ['10.4.0.1', 'domino.d']

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

SERVER_EMAIL = get_secret('SERVER_EMAIL')
DEFAULT_FROM_EMAIL = SERVER_EMAIL
SERVER_EMAIL = SERVER_EMAIL

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',  # noqa
            'style': '{',
        }
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': '/var/log/django/domino/request.log',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'INFO'
        }
    }
}
