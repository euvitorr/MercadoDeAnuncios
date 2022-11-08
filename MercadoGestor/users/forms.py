import re
from os.path import splitext

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from core.utils import valid_cpf

from .models import Address

User = get_user_model()


# Sign Up Form
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        label="Nome", max_length=30, required=False, help_text="Optional"
    )
    # email = forms.EmailField(max_length=254, help_text='Digite um e-mail valido')
    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "password1",
            "password2",
        ]

    def clean(self):
        full_name = self.cleaned_data["first_name"]
        if full_name is "":
            self.add_error("first_name", "Nome não pode ser vazio")
            raise forms.ValidationError("Verifique os erros a baixo e tente novamente")

        full_name = full_name.split()
        self.cleaned_data["first_name"] = full_name[0]
        if len(full_name) > 1:
            self.cleaned_data["last_name"] = full_name[1]
        return self.cleaned_data


class LoginForm(AuthenticationForm):
    error_messages = {
        "invalid_login": _(
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        "inactive": mark_safe(f"""O usuário ainda não foi ativado"""),
    }

    def confirm_login_allowed(self, user):
        if not user.is_allowed:
            raise forms.ValidationError(
                self.error_messages["inactive"],
                code="invalid_login",
                params={"username": self.username_field.verbose_name},
            )


class AddressForm(forms.ModelForm):
    CHOICES = (
        ("0", "SELCIONE UM ESTADO"),
        ("AC", "AC"),
        ("AL", "AL"),
        ("AP", "AP"),
        ("AM", "AM"),
        ("BA", "BA"),
        ("CE", "CE"),
        ("DF", "DF"),
        ("ES", "ES"),
        ("GO", "GO"),
        ("MA", "MA"),
        ("MT", "MT"),
        ("MS", "MS"),
        ("MG", "MG"),
        ("PA", "PA"),
        ("PB", "PB"),
        ("PR", "PR"),
        ("PE", "PE"),
        ("PI", "PI"),
        ("RJ", "RJ"),
        ("RN", "RN"),
        ("RS", "RS"),
        ("RO", "RO"),
        ("RR", "RR"),
        ("SC", "SC"),
        ("SP", "SP"),
        ("SE", "SE"),
        ("TO", "TO"),
    )
    state = forms.ChoiceField(choices=CHOICES)

    class Meta:
        model = Address
        fields = (
            "zipcode",
            "street",
            "street_number",
            "complement",
            "city",
            "neighborhood",
            "city",
            "state",
        )

    def clean_state(self):
        state = self.cleaned_data.get("state")
        if state == "0" or state is None:
            self.add_error("state", "Estado selecionado não é valido")
        return state


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name")


class AvatarForm(forms.Form):
    avatar = forms.ImageField()
    x = forms.FloatField(widget=forms.HiddenInput(), required=False)
    y = forms.FloatField(widget=forms.HiddenInput(), required=False)
    width = forms.FloatField(widget=forms.HiddenInput(), required=False)
    height = forms.FloatField(widget=forms.HiddenInput(), required=False)

    def clean_avatar(self):
        file = self.cleaned_data.get("avatar")
        valid_formats = ".jpg", ".jpeg", ".png"
        if file is None:
            self.add_error("avatar", "Avatar nao pode ser Vazio")
        filename, ext = splitext(file.name.strip())
        if not ext in valid_formats:
            self.add_error(
                "avatar",
                f"Extão {ext} não é valida para Image, por favor utilize os formatos {', '.join(valid_formats)}",
            )
        return file
