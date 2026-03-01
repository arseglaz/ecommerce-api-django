import pytest
from django.urls import reverse
from rest_framework import status
from cart.models import CartItem


@pytest.mark.django_db
class TestCartAPI:
    def test_my_cart_requires_auth(self, api_client):
        url = '/api/cart/my_cart/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_my_cart(self, api_client, user_john, cart_for_john):
        api_client.force_authenticate(user=user_john)
        url = '/api/cart/my_cart/'
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['total_items'] == 2

    def test_add_item_to_cart(self, api_client, user_john, iphone_product):
        api_client.force_authenticate(user=user_john)
        url = '/api/cart/add_item/'
        payload = {
            'product_id': iphone_product.id,
            'quantity': 1
        }
        response = api_client.post(url, payload, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['total_items'] == 1

    def test_remove_item_from_cart(self, api_client, user_john, cart_for_john):
        api_client.force_authenticate(user=user_john)
        item = CartItem.objects.get(cart=cart_for_john)
        url = f'/api/cart/remove_item/{item.id}/'
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['total_items'] == 0
