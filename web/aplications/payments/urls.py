from django.urls import path
from . import views

app_name = "payments"

urlpatterns = [
    path("mp_create/", views.mp_create, name="mp_create"),
    path("success/", views.success_view, name="success"),
    path("failure/", views.failure_view, name="failure"),
    path("pending/", views.pending_view, name="pending"),
    #path("webhook/", views.webhook_view, name="webhook"),  # opcional
]
