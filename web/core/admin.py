from django.contrib import admin
from .models import CarouselSlide

@admin.register(CarouselSlide)
class CarouselSlideAdmin(admin.ModelAdmin):
    list_display = ('id','title','is_active','order')
    list_editable = ('is_active','order')
    search_fields = ('title','subtitle')
