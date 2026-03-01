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

## Installation

```bash
git clone <repo-url>
cd ecommerce_api_project
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

Translated with DeepL.com (free version)