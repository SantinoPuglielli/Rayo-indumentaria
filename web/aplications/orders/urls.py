from django.urls import path
from django.shortcuts import render, get_object_or_404
from .models import Pedido

app_name = 'orders'
def detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'orders/detail.html', {'order': order})
urlpatterns = [ path('<int:pk>/', detail, name='detail') ]
