from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from products.models import Category, Product, Review
from cart.models import Cart, CartItem
from decimal import Decimal



class Command(BaseCommand):
    help = 'Create test data for development'


    def handle(self, *args, **kwargs):
        self.stdout.write('Creating test data...')


        # Creating categories with get_or_create
        electronics, created = Category.objects.get_or_create(
            slug='electronics',
            defaults={
                'name': 'Electronics',
                'description': 'Smartphones, laptops, tablets'
            }
        )
        if created:
            self.stdout.write(f'✓ Created category: {electronics.name}')
        else:
            self.stdout.write(f'→ Category already exists: {electronics.name}')
        
        clothing, created = Category.objects.get_or_create(
            slug='clothing',
            defaults={
                'name': 'Clothing',
                'description': 'Men\'s and women\'s clothing'
            }
        )
        if created:
            self.stdout.write(f'✓ Created category: {clothing.name}')
        else:
            self.stdout.write(f'→ Category already exists: {clothing.name}')
        
        books, created = Category.objects.get_or_create(
            slug='books',
            defaults={
                'name': 'Books',
                'description': 'Fiction and technical literature'
            }
        )
        if created:
            self.stdout.write(f'✓ Created category: {books.name}')
        else:
            self.stdout.write(f'→ Category already exists: {books.name}')


        # Creating products with get_or_create
        iphone, created = Product.objects.get_or_create(
            slug='iphone-15-pro-max',
            defaults={
                'category': electronics,
                'name': 'iPhone 15 Pro Max',
                'description': 'Apple flagship smartphone with A17 Pro chip, 256GB',
                'price': Decimal('1299.99'),
                'stock_quantity': 50
            }
        )
        if created:
            self.stdout.write(f'✓ Created product: {iphone.name}')
        else:
            self.stdout.write(f'→ Product already exists: {iphone.name}')
        
        samsung, created = Product.objects.get_or_create(
            slug='samsung-galaxy-s24-ultra',
            defaults={
                'category': electronics,
                'name': 'Samsung Galaxy S24 Ultra',
                'description': 'Android flagship with S Pen and 200MP camera',
                'price': Decimal('1199.99'),
                'stock_quantity': 30
            }
        )
        if created:
            self.stdout.write(f'✓ Created product: {samsung.name}')
        else:
            self.stdout.write(f'→ Product already exists: {samsung.name}')
        
        macbook, created = Product.objects.get_or_create(
            slug='macbook-pro-m3',
            defaults={
                'category': electronics,
                'name': 'MacBook Pro M3',
                'description': 'Apple laptop with M3 chip, 16GB RAM, 512GB SSD',
                'price': Decimal('2499.99'),
                'stock_quantity': 10
            }
        )
        if created:
            self.stdout.write(f'✓ Created product: {macbook.name}')
        else:
            self.stdout.write(f'→ Product already exists: {macbook.name}')
        
        jacket, created = Product.objects.get_or_create(
            slug='nike-winter-jacket',
            defaults={
                'category': clothing,
                'name': 'Nike Winter Jacket',
                'description': 'Warm winter jacket, size M',
                'price': Decimal('149.99'),
                'stock_quantity': 100
            }
        )
        if created:
            self.stdout.write(f'✓ Created product: {jacket.name}')
        else:
            self.stdout.write(f'→ Product already exists: {jacket.name}')
        
        python_book, created = Product.objects.get_or_create(
            slug='python-for-beginners',
            defaults={
                'category': books,
                'name': 'Python for Beginners',
                'description': 'Book on Python programming',
                'price': Decimal('29.99'),
                'stock_quantity': 200
            }
        )
        if created:
            self.stdout.write(f'✓ Created product: {python_book.name}')
        else:
            self.stdout.write(f'→ Product already exists: {python_book.name}')


        # Creating test users
        john, created = User.objects.get_or_create(
            username='john',
            defaults={
                'email': 'john@example.com'
            }
        )
        if created:
            john.set_password('testpass123')
            john.save()
            self.stdout.write(f'✓ Created user: john')
        else:
            self.stdout.write(f'→ User already exists: john')
        
        mary, created = User.objects.get_or_create(
            username='mary',
            defaults={
                'email': 'mary@example.com'
            }
        )
        if created:
            mary.set_password('testpass123')
            mary.save()
            self.stdout.write(f'✓ Created user: mary')
        else:
            self.stdout.write(f'→ User already exists: mary')


        # Creating reviews (only if they don't exist yet)
        review1, created = Review.objects.get_or_create(
            product=iphone,
            user=john,
            defaults={
                'rating': 5,
                'comment': 'Great smartphone! Very fast, and the camera is awesome!'
            }
        )
        if created:
            self.stdout.write(f'✓ Created review: john → iPhone (5★)')
        else:
            self.stdout.write(f'→ Review already exists: john → iPhone')


        review2, created = Review.objects.get_or_create(
            product=iphone,
            user=mary,
            defaults={
                'rating': 4,
                'comment': 'Good phone, but expensive'
            }
        )
        if created:
            self.stdout.write(f'✓ Created review: mary → iPhone (4★)')
        else:
            self.stdout.write(f'→ Review already exists: mary → iPhone')


        review3, created = Review.objects.get_or_create(
            product=samsung,
            user=john,
            defaults={
                'rating': 5,
                'comment': 'Best Android! S Pen is very convenient'
            }
        )
        if created:
            self.stdout.write(f'✓ Created review: john → Samsung (5★)')
        else:
            self.stdout.write(f'→ Review already exists: john → Samsung')


        # Creating cart for john (only if it doesn't exist yet)
        cart, created = Cart.objects.get_or_create(user=john)
        if created:
            self.stdout.write(f'✓ Created cart for john')
        else:
            self.stdout.write(f'→ Cart already exists for john')
        
        # Adding items to cart (only if they don't exist yet)
        cart_item1, created = CartItem.objects.get_or_create(
            cart=cart,
            product=iphone,
            defaults={'quantity': 2}
        )
        if created:
            self.stdout.write(f'✓ Added to cart: 2x iPhone')
        else:
            self.stdout.write(f'→ Already in cart: iPhone')
        
        cart_item2, created = CartItem.objects.get_or_create(
            cart=cart,
            product=macbook,
            defaults={'quantity': 1}
        )
        if created:
            self.stdout.write(f'✓ Added to cart: 1x MacBook')
        else:
            self.stdout.write(f'→ Already in cart: MacBook')


        self.stdout.write(self.style.SUCCESS('\n✅ Test data created/verified successfully!'))
        self.stdout.write(f'\nYou can login with:')
        self.stdout.write(f'  username: john, password: testpass123')
        self.stdout.write(f'  username: mary, password: testpass123')
