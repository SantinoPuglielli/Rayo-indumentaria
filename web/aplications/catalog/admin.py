from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Category, Product, Size, Color, ProductImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('preview', 'image', 'is_main', 'order')
    readonly_fields = ('preview',)

    def preview(self, obj):
        if obj and obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="height:60px;border-radius:4px;">')
        return "—"

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('thumb', 'name', 'category', 'price', 'is_active')
    list_filter = ('category', 'is_active', 'colors', 'sizes')
    search_fields = ('name', 'description')
    filter_horizontal = ('sizes', 'colors')
    inlines = [ProductImageInline]

    def thumb(self, obj):
        first = obj.images.first()
        if first and first.image:
            return mark_safe(f'<img src="{first.image.url}" style="height:40px;border-radius:3px;">')
        return '—'
    thumb.short_description = "Img"
