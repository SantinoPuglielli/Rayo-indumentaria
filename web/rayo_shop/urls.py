from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from aplications.reports.admin import admin_site as reports_admin


urlpatterns = [
    path('admin/', admin.site.urls),
    path('panel/', reports_admin.urls),      # dashboard de reporting
    path('', include('core.urls')),          # Home
    path('catalog/', include('aplications.catalog.urls')),
    path('cart/', include('aplications.cart.urls')),
    path('payments/', include('aplications.payments.urls')),
    path('orders/', include('aplications.orders.urls')),
]

# Servir archivos de MEDIA en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # (opcional) servir STATIC si lo necesitás:
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
