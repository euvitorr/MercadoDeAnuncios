from django import forms
from .models import Product, ProductLink


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ("sku", "name", "quantity")

class LinkForm(forms.ModelForm):
    class Meta:
        model= ProductLink
        fields = '__all__'
