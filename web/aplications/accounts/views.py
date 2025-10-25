from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import PerfilUsuario, Rol, UsuarioEstado
from aplications.orders.models import Pedido  # Importá el modelo de pedidos


# 🧾 REGISTRO DE USUARIOS
def register_view(request):
    """
    Vista para registrar usuarios con el rol 'Cliente'
    """
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        email = request.POST.get('email')
        password = request.POST.get('password')
        direccion = request.POST.get('direccion')
        telefono = request.POST.get('telefono')

        # Validaciones básicas
        if User.objects.filter(email=email).exists():
            messages.error(request, "Ya existe una cuenta registrada con ese correo.")
            return redirect('accounts:register')

        username = email.split('@')[0]  # nombre base para el username

        with transaction.atomic():
            user = User.objects.create_user(
                username=username,
                first_name=nombre,
                last_name=apellido,
                email=email,
                password=password
            )

            rol_cliente, _ = Rol.objects.get_or_create(nombre="Cliente")
            estado_activo, _ = UsuarioEstado.objects.get_or_create(nombre="Activo")

            PerfilUsuario.objects.create(
                usuario=user,
                rol=rol_cliente,
                estado=estado_activo,
                direccion=direccion,
                telefono=telefono
            )

        messages.success(request, "Cuenta creada correctamente. Iniciá sesión para continuar.")
        return redirect('accounts:login')

    return render(request, 'accounts/register.html')


# 🔑 LOGIN DE USUARIO
def login_view(request):
    """
    Vista para iniciar sesión usando el correo electrónico
    """
    if request.method == 'POST':
        correo = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=correo)
        except User.DoesNotExist:
            messages.error(request, "No existe una cuenta con ese correo.")
            return redirect('accounts:login')

        user = authenticate(request, username=user.username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Bienvenido {user.first_name} 👋")

            # Si es administrador → panel
            perfil = PerfilUsuario.objects.filter(usuario=user).first()
            if perfil and perfil.rol.nombre.lower() == "administrador":
                return redirect('/admin/')
            else:
                return redirect('/')
        else:
            messages.error(request, "Contraseña incorrecta.")
            return redirect('accounts:login')

    return render(request, 'accounts/login.html')


# 🚪 LOGOUT
def logout_view(request):
    logout(request)
    messages.info(request, "Cerraste sesión correctamente.")
    return redirect('/')


# 👤 PERFIL DE USUARIO
@login_required
def perfil_view(request):
    perfil = PerfilUsuario.objects.get(usuario=request.user)

    if request.method == 'POST':
        perfil.direccion = request.POST.get('direccion', perfil.direccion)
        perfil.telefono = request.POST.get('telefono', perfil.telefono)
        perfil.save()

        request.user.first_name = request.POST.get('first_name', request.user.first_name)
        request.user.last_name = request.POST.get('last_name', request.user.last_name)
        request.user.email = request.POST.get('email', request.user.email)
        request.user.save()

        messages.success(request, "Datos actualizados correctamente.")
        return redirect('accounts:perfil')

    return render(request, 'accounts/perfil.html', {'perfil': perfil})


@login_required
def mis_pedidos_view(request):
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-fecha')
    return render(request, 'accounts/mis_pedidos.html', {'pedidos': pedidos})

