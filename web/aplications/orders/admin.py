from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ('id','status','total_amount','created_at')
    list_filter = ('status','created_at')
    search_fields = ('id','mp_payment_id','mp_preference_id')
