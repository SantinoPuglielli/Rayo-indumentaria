from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Usuario

def login_view(request):
    """Vista para el inicio de sesión"""
    if request.user.is_authenticated:
        # Si ya está autenticado, redirigir según su rol
        if request.user.id_rol == 1:
            return redirect('/admin/')
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Autenticar usuario
        usuario = authenticate(request, username=email, password=password)
        
        if usuario is not None:
            login(request, usuario)
            
            # Redirigir según el rol
            if usuario.id_rol == 1:  # Administrador
                return redirect('/admin/')
            else:  # Usuario normal
                return redirect('home')
        else:
            return render(request, 'core/login.html', {
                'error': 'Email o contraseña incorrectos'
            })
    
    return render(request, 'core/login.html')


def registro_view(request):
    """Vista para el registro de nuevos usuarios"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        email = request.POST.get('email')
        password = request.POST.get('password')
        direccion = request.POST.get('direccion')
        telefono = request.POST.get('telefono', '')
        
        # Validar que el email no exista
        if Usuario.objects.filter(email=email).exists():
            return render(request, 'core/registro.html', {
                'error': 'Este email ya está registrado'
            })
        
        try:
            # Crear nuevo usuario con rol 2 (Usuario normal)
            usuario = Usuario.objects.create(
                nombre=nombre,
                apellido=apellido,
                email=email,
                contrasenia=password,  # En texto plano como está en tu BD
                id_rol=2,  # Siempre Usuario normal al registrarse
                direccion=direccion,
                telefono=telefono if telefono else None,
                id_estado_usuario=1  # Activo
            )
            
            # Login automático después del registro
            login(request, usuario, backend='core.backends.PlainTextAuthBackend')
            
            messages.success(request, '¡Cuenta creada exitosamente!')
            return redirect('home')
            
        except Exception as e:
            return render(request, 'core/registro.html', {
                'error': f'Error al crear la cuenta: {str(e)}'
            })
    
    return render(request, 'core/registro.html')


def logout_view(request):
    """Vista para cerrar sesión"""
    logout(request)
    return redirect('login')


@login_required
def home_view(request):
    """Vista de la página principal (requiere autenticación)"""
    return render(request, 'core/home.html', {
        'usuario': request.user
    })


def home_view(request):
    """Vista principal del home"""
    return render(request, 'core/home.html')