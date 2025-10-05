from django.urls import path
from . import views
app_name = 'cart'
urlpatterns = [
    path('', views.detail, name='detail'),
    path('add/<int:pk>/', views.add, name='add'),
]
