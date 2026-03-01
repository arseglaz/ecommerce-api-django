import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from products.models import Category, Product, Review
from cart.models import Cart, CartItem
from decimal import Decimal


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_john(db):
    return User.objects.create_user(
        username='john',
        email='john@example.com',
        password='testpass123'
    )


@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin1234'
    )


@pytest.fixture
def electronics_category(db):
    return Category.objects.create(
        name='Electronics',
        description='Smartphones, laptops, tablets'
    )


@pytest.fixture
def iphone_product(db, electronics_category):
    return Product.objects.create(
        category=electronics_category,
        name='iPhone 15 Pro Max',
        description='Apple flagship smartphone',
        price=Decimal('1299.99'),
        stock_quantity=10,
        is_active=True,
    )


@pytest.fixture
def cart_for_john(db, user_john, iphone_product):
    cart = Cart.objects.create(user=user_john)
    CartItem.objects.create(
        cart=cart,
        product=iphone_product,
        quantity=2
    )
    return cart
