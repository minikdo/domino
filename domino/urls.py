from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path, include
from django.conf import settings
import os


urlpatterns = [
    path('inventory/', include('inventory.urls')),
    path('transactions/', include('transactions.urls')),
    path('machines/', include('machines.urls')),
    path('invoices/', include('invoices.urls')),
    path('gold/', include('gold.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('', LoginView.as_view())
]

if settings.DEBUG:
    if os.environ.get('DJANGO_SETTINGS_MODULE') == 'domino.settings.local':
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
