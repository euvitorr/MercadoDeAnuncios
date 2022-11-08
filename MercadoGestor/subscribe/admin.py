from django.contrib import admin

from .models import Contact, Subscribe

# Register your models here.

@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    search_fields = ("email", )
    list_display = ('email', 'created', 'stopped', 'active',)
    list_filter = ('active',)
    readonly_fields=('created',)
    fieldsets = (
        (None, {"fields": ("email", "created", 'stopped', 'active', )}),
    )

@admin.register(Contact)
class ContatoAdmin(admin.ModelAdmin): 
    search_fields = ("none", "email", "phone")
    list_display = ("nome", "email", "phone", "created", "whatapp_enable")
    list_filter = ('whatapp_enable',)
    readonly_fields=('created',)
