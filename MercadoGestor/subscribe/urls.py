from django.urls import path

from .views import contact, subscribe

urlpatterns = [
    path('contact', contact, name='contact'),
    path('subscribe', subscribe, name='subscribe'),
]
