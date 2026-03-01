# E-commerce API (Django REST Framework)

Backend-only training project for an online store on Django + DRF.

## Features

- JWT authentication (registration, login, logout, token refresh)
- Categories and products (CRUD for admins, public read)
- Product reviews (one review per product from a user, owner rights)
- Shopping cart (one cart per user, add/update/remove/clear operations)
- Filtering, searching, sorting, pagination

## Stack

- Python 3.x
- Django
- Django REST Framework
- SimpleJWT
- pytest + pytest-django

## API endpoints (основные)

### Auth
- `POST /api/auth/register/`
- `POST /api/auth/login/`
- `POST /api/auth/logout/`
- `POST /api/auth/token/refresh/`
- `GET/PATCH /api/auth/profile/`

### Categories & Products
- `GET /api/categories/`
- `GET /api/categories/{slug}/`
- `GET /api/products/`
- `GET /api/products/{slug}/`
- `GET /api/products/{slug}/reviews/`

### Reviews
- `GET /api/reviews/`
- `POST /api/reviews/`
- `PATCH/DELETE /api/reviews/{id}/`

### Cart
- `GET /api/cart/my_cart/`
- `POST /api/cart/add_item/`
- `PATCH /api/cart/update_item/{id}/`
- `DELETE /api/cart/remove_item/{id}/`
- `DELETE /api/cart/clear/`

### Orders
- `GET /api/orders/`
- `GET /api/orders/{id}/`
- `POST /api/orders/create_from_cart/`


## Installation

```bash
git clone <repo-url>
cd ecommerce_api_project
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

