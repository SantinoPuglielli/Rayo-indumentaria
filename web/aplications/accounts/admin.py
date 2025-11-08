from django.contrib import admin
from .models import PerfilUsuario, UsuarioEstado, Rol, Funcion, RolFuncion

# ✅ Ocultamos todos los modelos de la app 'accounts' del panel de administración
#    (siguen existiendo, pero no se muestran en el menú lateral)
for model in (PerfilUsuario, UsuarioEstado, Rol, Funcion, RolFuncion):
    try:
        admin.site.unregister(model)
    except admin.sites.NotRegistered:
        pass
