import pytest
from django.urls import reverse
from rest_framework import status
from decimal import Decimal
from orders.models import Order, OrderItem
from cart.models import Cart, CartItem


@pytest.mark.django_db
class TestOrderAPI:
    def test_create_order_from_cart(self, api_client, user_john, iphone_product):
        # Setup: add item to john's cart
        cart = Cart.objects.create(user=user_john)
        CartItem.objects.create(cart=cart, product=iphone_product, quantity=2)

        api_client.force_authenticate(user=user_john)
        url = reverse('order-create-from-cart')
        response = api_client.post(url, {}, format='json')

        assert response.status_code == status.HTTP_201_CREATED

        order = Order.objects.first()
        assert order.user == user_john
        assert order.total_price == iphone_product.price * 2

        order_item = OrderItem.objects.first()
        assert order_item.order == order
        assert order_item.product == iphone_product
        assert order_item.quantity == 2
        assert order_item.price == iphone_product.price

        # Cart must be cleared after order creation
        assert cart.items.count() == 0

        assert response.data['id'] == order.id
        assert response.data['total_price'] == str(order.total_price)

    def test_create_order_from_empty_cart(self, api_client, user_john):
        Cart.objects.create(user=user_john)

        api_client.force_authenticate(user=user_john)
        url = reverse('order-create-from-cart')
        response = api_client.post(url, {}, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'Cart has no items' in response.data['error']

    def test_create_order_no_cart(self, api_client, user_john):
        api_client.force_authenticate(user=user_john)
        url = reverse('order-create-from-cart')
        response = api_client.post(url, {}, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'Cart is empty' in response.data['error']

    def test_list_orders_unauthenticated(self, api_client):
        url = reverse('order-list')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_orders_authenticated(self, api_client, user_john, iphone_product):
        # Create cart and order for john using existing fixture
        cart = Cart.objects.create(user=user_john)
        CartItem.objects.create(cart=cart, product=iphone_product, quantity=1)

        api_client.force_authenticate(user=user_john)
        api_client.post(reverse('order-create-from-cart'))

        url = reverse('order-list')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1

    def test_list_orders_other_user(self, api_client, user_john, admin_user, iphone_product):
        # Create order for admin
        cart_admin = Cart.objects.create(user=admin_user)
        CartItem.objects.create(cart=cart_admin, product=iphone_product, quantity=1)

        api_client.force_authenticate(user=admin_user)
        api_client.post(reverse('order-create-from-cart'))

        # john must not see admin's orders
        api_client.force_authenticate(user=user_john)
        url = reverse('order-list')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 0

    def test_stock_decreases_after_order(self, api_client, user_john, iphone_product):
        initial_stock = iphone_product.stock_quantity
        cart = Cart.objects.create(user=user_john)
        CartItem.objects.create(cart=cart, product=iphone_product, quantity=3)

        api_client.force_authenticate(user=user_john)
        api_client.post(reverse('order-create-from-cart'))

        iphone_product.refresh_from_db()
        assert iphone_product.stock_quantity == initial_stock - 3

    def test_order_detail(self, api_client, user_john, iphone_product):
        cart = Cart.objects.create(user=user_john)
        CartItem.objects.create(cart=cart, product=iphone_product, quantity=1)

        api_client.force_authenticate(user=user_john)
        api_client.post(reverse('order-create-from-cart'))

        order = Order.objects.first()
        url = reverse('order-detail', kwargs={'pk': order.pk})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == order.id
        assert len(response.data['items']) == 1
        assert response.data['items'][0]['quantity'] == 1
