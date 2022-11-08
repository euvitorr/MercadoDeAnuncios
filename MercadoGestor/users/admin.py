# Register your models here.
from django import forms
from django.contrib import admin, messages
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group, Permission
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.safestring import mark_safe

from .models import Address
from .token import account_activation_token

User = get_user_model()


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ("email",)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")

        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.is_active = False
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ("email", "password", "is_active", "is_admin")

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        "street",
        "street_number",
        "complement",
        "zipcode",
        "neighborhood",
        "state",
        "city",
        "country",
    )
    list_filter = ("city", "state", "neighborhood")


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = (
        "email",
        "get_full_name",
        "cpf",
        "birth",
        "phone",
        "cpf",
        "is_admin",
    )
    list_filter = ("is_admin", "is_active")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "birth",
                    "cpf",
                    "phone",
                    "avatar",
                )
            },
        ),
        (
            "Permissions",
            {"fields": ("is_admin", "is_active", "is_allowed", "is_superuser")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "birth",
                    "cpf",
                    "phone",
                    "profile",
                    "avatar",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    search_fields = ("email", "first_name", "last_name", "birth", "phone")
    ordering = ("email",)
    filter_horizontal = ()

    @mark_safe
    def photo_viewer(self, obj):
        image_url = (
            obj.avatar.url
            if len(obj.avatar.name) > 0
            else "/static/images/icon_user.svg"
        )
        return '<img style="border-radius:100%;" width="32px" src="{}" />'.format(
            image_url
        )

    photo_viewer.short_description = "Avatar"

    def get_full_name(self, obj):
        return obj.get_full_name()

    get_full_name.short_description = "full name"

    def send_activated_to_users(modeladmin, request, queryset):
        for user in queryset:
            current_site = get_current_site(request)
            subject = "Ative sua conta | ManagerML"
            message = render_to_string(
                "email/account_activation_email.txt",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            user.email_user(subject, message)
        messages.success(request, "Email para ativação enviados com sucesso.")

    send_activated_to_users.short_description = "Enviar link de ativação para o usuário"
    actions = [send_activated_to_users]
