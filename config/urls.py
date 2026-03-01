from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from .views import api_root


def home(request):
    return redirect('/api/')


urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),

    # Custom API root — shows all endpoints
    path('api/', api_root, name='api-root'),

    path('api/', include('products.urls')),
    path('api/', include('cart.urls')),
    path('api/', include('orders.urls')),
    path('api/auth/', include('users.urls')),

    # TODO: DRF Browsable API logout broken on Django 5.x (GET → 405)
    # Fix later or use Postman/VS Code REST Client for JWT testing
    path('api-auth/', include('rest_framework.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
