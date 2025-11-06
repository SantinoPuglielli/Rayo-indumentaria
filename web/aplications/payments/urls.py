from django.urls import path
from . import views

app_name = "payments"

urlpatterns = [
    path("crear-preferencia/", views.crear_preferencia, name="crear_preferencia"),
    path("webhook/", views.webhook, name="webhook"),
    path("retorno/", views.retorno, name="retorno"),
]
