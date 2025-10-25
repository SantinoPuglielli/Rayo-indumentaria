from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_view, name='view'),
    path('add/<int:variante_id>/', views.add_to_cart, name='add'),
    path('remove/<int:variante_id>/', views.remove_from_cart, name='remove'),
    path('clear/', views.clear_cart, name='clear'),
    path('increase/<int:variante_id>/', views.increase_qty, name='increase'),
    path('decrease/<int:variante_id>/', views.decrease_qty, name='decrease'),
    path('remove_one/<int:variante_id>/', views.remove_one, name='remove_one'),

]
