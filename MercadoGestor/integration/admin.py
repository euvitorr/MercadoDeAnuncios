from django.contrib import admin
from .models import ValidML
# Register your models here.
@admin.register(ValidML)
class ValidMLAdmin(admin.ModelAdmin):
    search_fields = ("company",)
    list_display = ("company",)
    list_filter = ("company",)