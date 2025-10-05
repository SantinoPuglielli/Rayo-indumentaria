from django.db import models
from django.contrib.auth import get_user_model

class Order(models.Model):
    STATUS = [
        ('created','Creada'),('approved','Aprobada'),
        ('pending','Pendiente'),('rejected','Rechazada'),('cancelled','Cancelada')
    ]
    user = models.ForeignKey(get_user_model(), null=True, blank=True, on_delete=models.SET_NULL)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    mp_preference_id = models.CharField(max_length=120, blank=True)
    mp_payment_id = models.CharField(max_length=120, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default='created')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"Order #{self.id} - {self.status}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('catalog.Product', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
