from itertools import product
from django.shortcuts import redirect, render, resolve_url
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.forms import inlineformset_factory
from .models import Product,ProductLink, History, User
from integration.models import ValidML
import products
from .forms import ProductForm,LinkForm
import json
import requests
import pytz
from datetime import datetime  
from datetime import timedelta
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import logging
from datetime import date
def ProductView(request):
    local_tz = pytz.timezone('America/Sao_Paulo')
    if len(Product.objects.filter())>0:
        if len(ValidML.objects.filter(company=request.user.company))==0:
            return redirect('http://localhost:8000/integration/validate/')
        NewCode=ValidML.objects.filter(company=request.user.company)[0]
        if datetime.now().replace(tzinfo=pytz.utc).astimezone(local_tz)>NewCode.expires_in.replace(tzinfo=pytz.utc).astimezone(local_tz):
            return redirect('http://localhost:8000/integration/validate/')
        else:
            model = Product
            

            for products in ProductLink.objects.filter(product=Product.objects.filter(company = request.user.company)[0]):
                specs = requests.get('https://api.mercadolibre.com/items/'+str(products)[41:], headers={'Authorization': 'Bearer {}'.format(NewCode.access_token),'Accept': 'application/json', 'Content-Type': 'application/json'})
                if products.product.quantity!=specs.json()['variations'][0]['available_quantity']:
                    historico = History(product=products.product,company=request.user.company,user=User.objects.get(first_name='Mercado Livre'),create_at=date.today(),change="Quantidade de "+str(products.product.quantity)+" para "+str(specs.json()['variations'][0]['available_quantity']))
                    historico.save()
                    products.product.quantity = specs.json()['variations'][0]['available_quantity']
                    products.product.save()
            products=Product.objects.filter(company=request.user.company)
            form = ProductForm()
            form_product_factory = inlineformset_factory(Product,ProductLink, form=LinkForm,extra=3)
            inlineForm = form_product_factory()
            template_name = "products.html"
            return render(request, template_name, {"form": form,"form_inline":inlineForm,"products":products})
            def get_context_data(self, **kwargs):
                context = super().get_context_data(**kwargs)
                return context
            def get_queryset(self):
                return self.model.objects.all()
    else:
        template_name = "products.html"
        return render(request, template_name, {})

@csrf_exempt
def ProductAvailableQuantity(request, id, quantity):
    NewCode=ValidML.objects.filter(company=request.user.company)[0]
    historico = History(product=Product.objects.filter(id=id)[0],company=request.user.company,user=request.user,create_at=date.today(),change="Quantidade de "+str(Product.objects.filter(id=id)[0].quantity)+" para "+str(quantity))
    historico.save()
    for products in ProductLink.objects.filter(product=id):
        products.product.quantity = quantity
        products.product.save()
        specs = requests.get('https://api.mercadolibre.com/items/'+str(products)[41:], headers={'Authorization': 'Bearer {}'.format(NewCode.access_token),'Accept': 'application/json', 'Content-Type': 'application/json'})
        body = {
            "variations": [{
                "id":specs.json()['variations'][0]['id'],
                "available_quantity": quantity
            }]
        }   
        put = requests.put('https://api.mercadolibre.com/items/'+str(products)[41:],data=json.dumps(body), headers={'Authorization': 'Bearer {}'.format(NewCode.access_token),'Accept': 'application/json', 'Content-Type': 'application/json'})
    return HttpResponse(put)
        
def HistoryView(request):
    if len(History.objects.filter())>0:
        model = History
        local_tz = pytz.timezone('America/Sao_Paulo')
        template_name = "history.html"
        history = History.objects.filter(company=request.user.company)
        return render(request, template_name, {"history":history})
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            return context
        def get_queryset(self):
            return self.model.objects.all()
    else:
        template_name = "history.html"
        return render(request, template_name, {})
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            return context
        def get_queryset(self):
            return self.model.objects.all()