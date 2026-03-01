import pytest
from django.urls import reverse
from rest_framework import status
from products.models import Review


@pytest.mark.django_db
class TestReviewAPI:
    def test_list_reviews_public(self, api_client, user_john, iphone_product):
        Review.objects.create(
            product=iphone_product,
            user=user_john,
            rating=5,
            comment='Great phone!'
        )
        url = reverse('review-list')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['rating'] == 5

    def test_create_review_requires_auth(self, api_client, iphone_product):
        url = reverse('review-list')
        payload = {
            'product_slug': iphone_product.slug,
            'rating': 5,
            'comment': 'Nice!'
        }
        response = api_client.post(url, payload, format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_review_as_authenticated_user(self, api_client, user_john, iphone_product):
        api_client.force_authenticate(user=user_john)
        url = reverse('review-list')
        payload = {
            'product_slug': iphone_product.slug,
            'rating': 4,
            'comment': 'Good phone'
        }
        response = api_client.post(url, payload, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        review = Review.objects.get()
        assert review.user == user_john
        assert review.product == iphone_product

    def test_user_cannot_edit_other_users_review(self, api_client, user_john, iphone_product, admin_user):
        review = Review.objects.create(
            product=iphone_product,
            user=admin_user,
            rating=5,
            comment='Admin review'
        )
        api_client.force_authenticate(user=user_john)
        url = reverse('review-detail', kwargs={'pk': review.pk})
        payload = {'comment': 'I try to change this'}
        response = api_client.patch(url, payload, format='json')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_owner_can_edit_own_review(self, api_client, user_john, iphone_product):
        review = Review.objects.create(
            product=iphone_product,
            user=user_john,
            rating=3,
            comment='Ok'
        )
        api_client.force_authenticate(user=user_john)
        url = reverse('review-detail', kwargs={'pk': review.pk})
        payload = {'comment': 'Updated comment', 'rating': 4}
        response = api_client.patch(url, payload, format='json')

        assert response.status_code == status.HTTP_200_OK
        review.refresh_from_db()
        assert review.comment == 'Updated comment'
        assert review.rating == 4
