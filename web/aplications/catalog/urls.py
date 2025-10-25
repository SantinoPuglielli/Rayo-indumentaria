from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.product_list, name='list'),
    path('producto/<int:pk>/', views.product_detail, name='detail'),
    path('favoritos/', views.favoritos_view, name='favoritos'),
    path('favoritos/toggle/<int:pk>/', views.toggle_favorito, name='toggle_favorito'),
]