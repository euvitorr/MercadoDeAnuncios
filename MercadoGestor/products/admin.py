from django.contrib import admin
from .models import Product,ProductLink
from django.contrib.contenttypes.admin import GenericTabularInline
import logging
# Register your models here.

class ProductLinkInline(admin.StackedInline):
    model = ProductLink
    search_fields = ("link","product")
    list_display = ("link","product")
    list_filter = ("link","product")

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductLinkInline
    ]
    search_fields = ("sku", "name", "id","company")
    list_display = ("sku", "name", "id","company")
    list_filter = ('sku',)


@admin.register(ProductLink)
class ProductLink(admin.ModelAdmin):
    search_fields = ("link","product")
    list_display = ("link","product")
    list_filter = ("link","product")
