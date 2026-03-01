import pytest
from django.urls import reverse
from rest_framework import status
from products.models import Category, Product
from decimal import Decimal


@pytest.mark.django_db
class TestCategoryAPI:
    def test_list_categories_public(self, api_client, electronics_category):
        url = reverse('category-list')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['name'] == 'Electronics'

    def test_create_category_forbidden_for_non_admin(self, api_client, user_john):
        api_client.force_authenticate(user=user_john)
        url = reverse('category-list')
        payload = {
            'name': 'Clothing',
            'description': 'Clothes'
        }
        response = api_client.post(url, payload, format='json')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_category_allowed_for_admin(self, api_client, admin_user):
        api_client.force_authenticate(user=admin_user)
        url = reverse('category-list')
        payload = {
            'name': 'Books',
            'description': 'Books category'
        }
        response = api_client.post(url, payload, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert Category.objects.filter(name='Books').exists()


@pytest.mark.django_db
class TestProductAPI:
    def test_list_products_public(self, api_client, iphone_product):
        url = reverse('product-list')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['name'] == 'iPhone 15 Pro Max'

    def test_retrieve_product_by_slug(self, api_client, iphone_product):
        url = reverse('product-detail', kwargs={'slug': iphone_product.slug})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['slug'] == iphone_product.slug

    def test_create_product_forbidden_for_non_admin(self, api_client, user_john, electronics_category):
        api_client.force_authenticate(user=user_john)
        url = reverse('product-list')
        payload = {
            'name': 'MacBook Pro M3',
            'description': 'Apple laptop',
            'price': '2499.99',
            'stock_quantity': 5,
            'category_id': electronics_category.id,
            'is_active': True,
        }
        response = api_client.post(url, payload, format='json')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_product_allowed_for_admin(self, api_client, admin_user, electronics_category):
        api_client.force_authenticate(user=admin_user)
        url = reverse('product-list')
        payload = {
            'name': 'MacBook Pro M3',
            'description': 'Apple laptop',
            'price': '2499.99',
            'stock_quantity': 5,
            'category_id': electronics_category.id,
            'is_active': True,
        }
        response = api_client.post(url, payload, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert Product.objects.filter(name='MacBook Pro M3').exists()
