from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('reports/', include('aplications.reports.urls')),  # ✅ Reportes fuera del admin
    path('', include('core.urls')),
    path('catalog/', include('aplications.catalog.urls')),
    path('cart/', include('aplications.cart.urls')),
    path('pago/', include('aplications.payments.urls', namespace='payments')),
    path('orders/', include('aplications.orders.urls')),
    path('accounts/', include('aplications.accounts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
