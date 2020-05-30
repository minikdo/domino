from .base import * # noqa

DEBUG = False

ALLOWED_HOSTS += ['10.4.0.1', 'domino.d']

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

LOGGING = {
    'loggers': {
        'django': {
            'handlers': {['file']},
            'level': 'DEBUG'
        }
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': './django.log'
        }
    }
}
