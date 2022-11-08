
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path

from core.views import HomeTemplateView
from integration import views
admin.site.site_header = 'ManagerML'
urlpatterns = [
    path('', HomeTemplateView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('ml/', include(('core.urls', "core"))),
    path('accounts/', include(('users.urls', "users"))),
    path('subscribe/', include(('subscribe.urls', "subscribe"))),
    path('integration/', include(('integration.urls', 'integration'))),
    path('products/', include(('products.urls', 'products'))),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
