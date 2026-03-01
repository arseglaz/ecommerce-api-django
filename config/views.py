from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'categories': reverse('category-list', request=request, format=format),
        'products': reverse('product-list', request=request, format=format),
        'reviews': reverse('review-list', request=request, format=format),
        'cart': reverse('cart-my-cart', request=request, format=format),
        'orders': reverse('order-list', request=request, format=format),
        'auth': {
            'register': reverse('auth-register', request=request, format=format),
            'login': reverse('auth-login', request=request, format=format),
            'profile': reverse('auth-profile', request=request, format=format),
        }
    })
