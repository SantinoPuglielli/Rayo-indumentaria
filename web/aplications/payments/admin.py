from django.contrib import admin
from .models import MetodoPago, MetodoPagoEstado

# ✅ Ocultamos los modelos del panel de administración
for model in (MetodoPago, MetodoPagoEstado):
    try:
        admin.site.unregister(model)
    except admin.sites.NotRegistered:
        pass
