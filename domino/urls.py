from django.views.generic import TemplateView
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
import os


urlpatterns = [
    path('inventory/', include('inventory.urls')),
    path('transactions/', include('transactions.urls')),
    path('machines/', include('machines.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name="base.html")),
]

if settings.DEBUG:
    if os.environ.get('DJANGO_SETTINGS_MODULE') == 'domino.settings.local':
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
