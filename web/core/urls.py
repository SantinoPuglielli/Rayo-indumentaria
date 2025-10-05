from django.urls import path
from django.shortcuts import render
from django.db.utils import ProgrammingError, OperationalError

def home(request):
    featured = []
    try:
        from catalog.models import Product
        featured = Product.objects.filter(is_active=True).prefetch_related('images','category').order_by('-id')[:6]
    except (ProgrammingError, OperationalError, Exception):
        pass
    return render(request, 'core/home.html', {'featured': featured})

urlpatterns = [ path('', home, name='home') ]

from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home_view, name='home'),
]