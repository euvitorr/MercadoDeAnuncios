from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render

from .forms import ContactForm, SubscribeForm

# Create your views here.


def subscribe(request):
    data = {}
    if request.method == 'POST':
        form =  SubscribeForm(request.POST)
        if form.is_valid():
            form.save()
            data['result'] = form.data
            data['is_form_valid'] = True

        else:
            data['is_form_valid'] = False
            data['errors'] = dict(form.errors.items())

    return JsonResponse(data)


def contact(request): 
    data = {}
    if request.method == 'POST':
        form =  ContactForm(request.POST)
        if form.is_valid():
            form.save()
            data['result'] = dict(form.data.items())
            data['is_form_valid'] = True
            msg = f"uma novo contato {form.data['email']} foi cadastrado"
            send_mail(
                "Novo contato pontos solidário", 
                msg, from_email=settings.DEFAULT_FROM_MAIL, 
                recipient_list=["faleconosco@pontossolidarios.com.br"])

        else:
            data['is_form_valid'] = False
            data['errors'] = dict(form.errors.items())

    return JsonResponse(data)
