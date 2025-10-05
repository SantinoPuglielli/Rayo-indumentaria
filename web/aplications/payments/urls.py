from django.urls import path
from . import views
app_name = 'payments'
urlpatterns = [
    path('mp/create/', views.mp_create_preference, name='mp_create'),
    path('mp/feedback/', views.mp_feedback, name='mp_feedback'),
    path('mp/webhook/', views.mp_webhook, name='mp_webhook'),
]
