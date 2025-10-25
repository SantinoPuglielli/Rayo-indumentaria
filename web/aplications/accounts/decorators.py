from django.shortcuts import redirect
from django.contrib import messages
from .models import PerfilUsuario

def solo_admin(view_func):
    def _wrapped_view(request, *args, **kwargs):
        perfil = PerfilUsuario.objects.filter(usuario=request.user).first()
        if perfil and perfil.rol.nombre.lower() == "administrador":
            return view_func(request, *args, **kwargs)
        messages.error(request, "No tenés permiso para acceder a esta página.")
        return redirect('/')
    return _wrapped_view
