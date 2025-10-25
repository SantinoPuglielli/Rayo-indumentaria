from django.contrib import admin
from django.utils.html import format_html

# ✅ No usamos reverse() ni urls del admin aquí.
# Solo mostramos un enlace externo seguro.
admin.site.site_header = "Panel de Administración - Rayo Indumentaria"
admin.site.site_title = "Rayo Admin"

