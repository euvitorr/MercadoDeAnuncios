from django import forms

from .models import Contact, Subscribe


class SubscribeForm(forms.ModelForm):

    class Meta: 
        model = Subscribe
        fields = ('email', )


class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ('nome', 'email', 'phone', 'whatapp_enable',)
