from .base import * # noqa

DEBUG = True

INSTALLED_APPS += ['debug_toolbar', 'django_extensions']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']

INTERNAL_IPS = ['127.0.0.1']

ALLOWED_HOSTS += ['127.0.0.1']

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  # add STATIC_ROOT to DIRS
]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
# EMAIL_FILE_PATH = os.path.join(BASE_DIR, "sent_emails)"
