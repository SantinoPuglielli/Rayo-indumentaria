from django.contrib import admin
from .models import Carrito, CarritoItem, CarritoEstado

# ✅ Ocultamos del admin los modelos técnicos relacionados al carrito
for model in (CarritoEstado,):
    try:
        admin.site.unregister(model)
    except admin.sites.NotRegistered:
        pass

# (opcional) si querés también ocultar Carrito o CarritoItem del admin:
# for model in (Carrito, CarritoItem, CarritoEstado):
#     try:
#         admin.site.unregister(model)
#     except admin.sites.NotRegistered:
#         pass
