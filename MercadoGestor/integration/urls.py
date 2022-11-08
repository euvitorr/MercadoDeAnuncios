from django.urls import path,re_path

from integration import views

app_name = "instegration"
urlpatterns = [
    path('notification/', views.integration, name='integration'),
    path('validate/', views.ValidateMercado, name='validate'),
]
