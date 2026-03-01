# E-commerce API (Django REST Framework)

Backend-only e-commerce project built with Django + DRF.
Educational project demonstrating REST API design patterns.

## Features

### Authentication
- JWT-based authentication (access + refresh tokens)
- User registration with password validation
- Login / logout (refresh token blacklist)
- Token refresh endpoint
- User profile (view and update)

### Categories & Products
- Public read access (no auth required)
- CRUD for admins/staff only
- Product filtering by category, active status
- Search by name and description
- Ordering by price, date, name
- Pagination (10 items per page)

### Reviews
- Public read access
- Authenticated users can create reviews
- Only the review author can edit or delete their own review
- Filter by product slug and rating

### Cart
- One cart per user (auto-created)
- Add, update, remove items
- Clear cart
- Cart is private — users only see their own cart

### Orders
- Order is created from the current cart contents
- Cart is cleared automatically after order creation
- Product price is locked at the time of order (historical pricing)
- Stock quantity decreases after order
- Orders are private — users only see their own orders
- Order statuses: `pending`, `paid`, `shipped`, `completed`, `canceled`
- ⚠️ Payment integration is not implemented yet
  - All orders are created with status `pending`
  - Status can only be changed manually via Django Admin
  - Future: integrate Stripe/PayPal to handle `pending` → `paid` transition

### Addresses
- Users can manage multiple delivery addresses
- Address labels: home, office, other
- Only one address can be set as default at a time
- Users only see their own addresses

## Tech Stack

- Python 3.11
- Django 5.x
- Django REST Framework
- djangorestframework-simplejwt
- pytest + pytest-django
- SQLite (dev)

## API endpoints

### Auth
| Method | URL                      | Description                     | Auth |
| ------ | ------------------------ | ------------------------------- | ---- |
| POST   | /api/auth/register/      | Register new user               | No   |
| POST   | /api/auth/login/         | Login, get JWT tokens           | No   |
| POST   | /api/auth/logout/        | Logout, blacklist refresh token | Yes  |
| POST   | /api/auth/token/refresh/ | Get new access token            | No   |
| GET    | /api/auth/profile/       | View profile                    | Yes  |
| PATCH  | /api/auth/profile/       | Update profile                  | Yes  |

### Categories
| Method | URL                     | Description         | Auth  |
| ------ | ----------------------- | ------------------- | ----- |
| GET    | /api/categories/        | List all categories | No    |
| GET    | /api/categories/{slug}/ | Category detail     | No    |
| POST   | /api/categories/        | Create category     | Admin |
| PATCH  | /api/categories/{slug}/ | Update category     | Admin |
| DELETE | /api/categories/{slug}/ | Delete category     | Admin |

### Products
| Method | URL                           | Description     | Auth  |
| ------ | ----------------------------- | --------------- | ----- |
| GET    | /api/products/                | List products   | No    |
| GET    | /api/products/{slug}/         | Product detail  | No    |
| GET    | /api/products/{slug}/reviews/ | Product reviews | No    |
| POST   | /api/products/                | Create product  | Admin |
| PATCH  | /api/products/{slug}/         | Update product  | Admin |
| DELETE | /api/products/{slug}/         | Delete product  | Admin |

### Reviews
| Method | URL                | Description   | Auth  |
| ------ | ------------------ | ------------- | ----- |
| GET    | /api/reviews/      | List reviews  | No    |
| POST   | /api/reviews/      | Create review | Yes   |
| PATCH  | /api/reviews/{id}/ | Update review | Owner |
| DELETE | /api/reviews/{id}/ | Delete review | Owner |

### Cart
| Method | URL                         | Description           | Auth |
| ------ | --------------------------- | --------------------- | ---- |
| GET    | /api/cart/my_cart/          | View current cart     | Yes  |
| POST   | /api/cart/add_item/         | Add item to cart      | Yes  |
| PATCH  | /api/cart/update_item/{id}/ | Update item quantity  | Yes  |
| DELETE | /api/cart/remove_item/{id}/ | Remove item from cart | Yes  |
| DELETE | /api/cart/clear/            | Clear entire cart     | Yes  |

### Orders
| Method | URL                           | Description            | Auth |
| ------ | ----------------------------- | ---------------------- | ---- |
| GET    | /api/orders/                  | List my orders         | Yes  |
| GET    | /api/orders/{id}/             | Order detail           | Yes  |
| POST   | /api/orders/create_from_cart/ | Create order from cart | Yes  |

## Installation

```bash
git clone <repo-url>
cd ecommerce_api_project
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
