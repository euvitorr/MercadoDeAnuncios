from django.urls import path,re_path

from products import views

app_name = "products"
urlpatterns = [
    path('', views.ProductView, name='products'),
    path('<id>/<quantity>', views.ProductAvailableQuantity, name='product'),
    path('history', views.HistoryView, name='history'),
]
