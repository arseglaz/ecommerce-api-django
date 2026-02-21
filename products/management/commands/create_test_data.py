from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from products.models import Category, Product, Review
from cart.models import Cart, CartItem
from decimal import Decimal


class Command(BaseCommand):
    help = 'Create test data for development'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating test data...')

        # Categories
        electronics, created = Category.objects.get_or_create(
            slug='electronics',
            defaults={
                'name': 'Electronics',
                'description': 'Smartphones, laptops, tablets and more'
            }
        )
        self._log(created, 'category', electronics.name)

        clothing, created = Category.objects.get_or_create(
            slug='clothing',
            defaults={
                'name': 'Clothing',
                'description': 'Men and women clothing'
            }
        )
        self._log(created, 'category', clothing.name)

        books, created = Category.objects.get_or_create(
            slug='books',
            defaults={
                'name': 'Books',
                'description': 'Fiction and technical literature'
            }
        )
        self._log(created, 'category', books.name)

        # Products
        iphone, created = Product.objects.get_or_create(
            slug='iphone-15-pro-max',
            defaults={
                'category': electronics,
                'name': 'iPhone 15 Pro Max',
                'description': 'Apple flagship smartphone with A17 Pro chip, 256GB storage, titanium design',
                'price': Decimal('1299.99'),
                'stock_quantity': 50
            }
        )
        self._log(created, 'product', iphone.name)

        samsung, created = Product.objects.get_or_create(
            slug='samsung-galaxy-s24-ultra',
            defaults={
                'category': electronics,
                'name': 'Samsung Galaxy S24 Ultra',
                'description': 'Android flagship with S Pen and 200MP camera, 512GB storage',
                'price': Decimal('1199.99'),
                'stock_quantity': 30
            }
        )
        self._log(created, 'product', samsung.name)

        macbook, created = Product.objects.get_or_create(
            slug='macbook-pro-m3',
            defaults={
                'category': electronics,
                'name': 'MacBook Pro M3',
                'description': 'Apple laptop with M3 chip, 16GB RAM, 512GB SSD, 14-inch display',
                'price': Decimal('2499.99'),
                'stock_quantity': 10
            }
        )
        self._log(created, 'product', macbook.name)

        jacket, created = Product.objects.get_or_create(
            slug='nike-winter-jacket',
            defaults={
                'category': clothing,
                'name': 'Nike Winter Jacket',
                'description': 'Warm winter jacket, available in sizes S, M, L, XL',
                'price': Decimal('149.99'),
                'stock_quantity': 100
            }
        )
        self._log(created, 'product', jacket.name)

        python_book, created = Product.objects.get_or_create(
            slug='python-for-beginners',
            defaults={
                'category': books,
                'name': 'Python for Beginners',
                'description': 'Complete guide to Python programming from scratch',
                'price': Decimal('29.99'),
                'stock_quantity': 200
            }
        )
        self._log(created, 'product', python_book.name)

        # Users
        john, created = User.objects.get_or_create(
            username='john',
            defaults={'email': 'john@example.com'}
        )
        if created:
            john.set_password('testpass123')
            john.save()
            self.stdout.write(f'✓ Created user: john')
        else:
            self.stdout.write(f'→ User already exists: john')

        mary, created = User.objects.get_or_create(
            username='mary',
            defaults={'email': 'mary@example.com'}
        )
        if created:
            mary.set_password('testpass123')
            mary.save()
            self.stdout.write(f'✓ Created user: mary')
        else:
            self.stdout.write(f'→ User already exists: mary')

        # Reviews
        review1, created = Review.objects.get_or_create(
            product=iphone,
            user=john,
            defaults={
                'rating': 5,
                'comment': 'Amazing smartphone! Incredibly fast, camera is outstanding.'
            }
        )
        self._log(created, 'review', f'john → iPhone (5★)')

        review2, created = Review.objects.get_or_create(
            product=iphone,
            user=mary,
            defaults={
                'rating': 4,
                'comment': 'Great phone, but quite expensive for the price.'
            }
        )
        self._log(created, 'review', f'mary → iPhone (4★)')

        review3, created = Review.objects.get_or_create(
            product=samsung,
            user=john,
            defaults={
                'rating': 5,
                'comment': 'Best Android phone! The S Pen is incredibly useful.'
            }
        )
        self._log(created, 'review', f'john → Samsung (5★)')

        review4, created = Review.objects.get_or_create(
            product=macbook,
            user=mary,
            defaults={
                'rating': 5,
                'comment': 'Incredible performance, battery lasts all day. Worth every penny.'
            }
        )
        self._log(created, 'review', f'mary → MacBook (5★)')

        # Cart for john
        cart, created = Cart.objects.get_or_create(user=john)
        self._log(created, 'cart', 'john')

        cart_item1, created = CartItem.objects.get_or_create(
            cart=cart,
            product=iphone,
            defaults={'quantity': 2}
        )
        self._log(created, 'cart item', f'2x iPhone')

        cart_item2, created = CartItem.objects.get_or_create(
            cart=cart,
            product=macbook,
            defaults={'quantity': 1}
        )
        self._log(created, 'cart item', f'1x MacBook')

        self.stdout.write(self.style.SUCCESS('\n✅ Test data created/verified!'))
        self.stdout.write('\nLogin credentials:')
        self.stdout.write('  Admin:  admin / (your password)')
        self.stdout.write('  john  / testpass123')
        self.stdout.write('  mary  / testpass123')

    def _log(self, created, obj_type, name):
        """Helper method to log creation status"""
        if created:
            self.stdout.write(f'✓ Created {obj_type}: {name}')
        else:
            self.stdout.write(f'→ Already exists: {name}')
