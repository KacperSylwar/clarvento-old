from django.contrib import admin

from .models import (
    Product, ProductImage, ProductCategory, ProductFile, Manufacturer
)

class ProductFileInline(admin.TabularInline):
    model = ProductFile
    extra = 1

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ProductFileInline]
    list_display = [
        'name',
        'price_net_no_markup',
        'price_gross_no_markup',
        'price_net_with_markup',
        'price_gross_with_markup',
        'created_at',
        'updated_at',
        'show_on_homepage',
        'is_promotion',
        'is_sponsored'
    ]
    search_fields = ['name', 'description', 'application']
    list_filter = ['created_at', 'updated_at', 'show_on_homepage', 'is_promotion', 'is_sponsored']
    ordering = ['-updated_at']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name', 'description']

@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name', 'description']
