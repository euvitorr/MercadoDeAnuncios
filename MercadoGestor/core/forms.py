import re
from os.path import splitext

from django import forms

from .models import (
    Address
)
from .utils import format_cnpj, valid_cnpj, validate_contact_phone, validate_email


class UploadForm(forms.Form):
    file = forms.ImageField()


class ContactFormSet(forms.BaseModelFormSet):
    def clean(self):
        super().clean()
        for form in self.forms:
            kind = form.cleaned_data.get("kind", "")
            contact = form.cleaned_data.get("contact", "")

            if kind is None:
                form.add_error("kind", "Tipo deve ser email ou telefone")

            if kind == "email":
                if contact is None:
                    form.add_error(
                        "contact", "Tipo e-mail não pode conter um e-mail vazio"
                    )
                else:
                    match = re.match("([^@|\s]+@[^@]+\.[^@|\s]+)", contact)
                    if not match:
                        form.add_error(
                            "contact",
                            "Tipo email deve conter uma e-mail valido em contato, email: %s não é valido"
                            % contact,
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
