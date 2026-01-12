import random
import urllib.request
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.utils.text import slugify
from products.models import Category, Product

class Command(BaseCommand):
    help = 'Populates the database with sample products and dummy images'

    def handle(self, *args, **kwargs):
        self.stdout.write('Clearing existing data...')
        Category.objects.all().delete()
        Product.objects.all().delete()

        categories_data = {
            'Electronics': [
                'Smartphone', 'Laptop', 'Headphones', 'Smart Watch', 'Camera', 'Tablet',
                'Monitor', 'Keyboard', 'Mouse', 'Speaker'
            ],
            'Fashion': [
                'T-Shirt', 'Jeans', 'Jacket', 'Sneakers', 'Watch', 'Handbag',
                'Sunglasses', 'Hat', 'Dress', 'Boots'
            ],
            'Home': [
                'Sofa', 'Lamp', 'Chair', 'Table', 'Rug', 'Curtains',
                'Cushion', 'Bookshelf', 'Vase', 'Planter'
            ],
            'Books': [
                'Novel', 'Biography', 'Cookbook', 'Sci-Fi', 'History', 'Thriller',
                'Guide', 'Art Book', 'Comic', 'Dictionary'
            ]
        }
        
        adjectives = ['Premium', 'Stylish', 'Modern', 'Classic', 'Portable', 'Durable', 'Exclusive', 'Compact', 'Luxury', 'Essential']

        self.stdout.write('Downloading dummy images and creating products... (This may take a moment)')

        
        # Item to Image URL mapping
        item_image_mappings = {
            # Electronics
            'Smartphone': 'https://m.media-amazon.com/images/I/512sO2L0k6L._AC_UL640_FMwebp_QL65_.jpg?text=Smartphone',
            'Laptop': 'https://m.media-amazon.com/images/I/512sO2L0k6L._AC_UL640_FMwebp_QL65_.jpg?text=Laptop',
            'Headphones': 'https://m.media-amazon.com/images/I/512sO2L0k6L._AC_UL640_FMwebp_QL65_.jpg?text=Headphones',
            'Smart Watch': 'https://m.media-amazon.com/images/I/512sO2L0k6L._AC_UL640_FMwebp_QL65_.jpg?text=Smart+Watch',
            'Camera': 'https://m.media-amazon.com/images/I/512sO2L0k6L._AC_UL640_FMwebp_QL65_.jpg?text=Camera',
            'Tablet': 'https://m.media-amazon.com/images/I/512sO2L0k6L._AC_UL640_FMwebp_QL65_.jpg?text=Tablet',
            'Monitor': 'https://m.media-amazon.com/images/I/512sO2L0k6L._AC_UL640_FMwebp_QL65_.jpg?text=Monitor',
            'Keyboard': 'https://m.media-amazon.com/images/I/512sO2L0k6L._AC_UL640_FMwebp_QL65_.jpg?text=Keyboard',
            'Mouse': 'https://m.media-amazon.com/images/I/512sO2L0k6L._AC_UL640_FMwebp_QL65_.jpg?text=Mouse',
            'Speaker': 'https://m.media-amazon.com/images/I/512sO2L0k6L._AC_UL640_FMwebp_QL65_.jpg?text=Speaker',
            
            # Fashion
            'T-Shirt': 'https://m.media-amazon.com/images/I/512sO2L0k6L._AC_UL640_FMwebp_QL65_.jpg?text=T-Shirt',
            'Jeans': 'https://m.media-amazon.com/images/I/512sO2L0k6L._AC_UL640_FMwebp_QL65_.jpg?text=Jeans',
            'Jacket': 'https://m.media-amazon.com/images/I/512sO2L0k6L._AC_UL640_FMwebp_QL65_.jpg?text=Jacket',
            'Sneakers': 'https://m.media-amazon.com/images/I/512sO2L0k6L._AC_UL640_FMwebp_QL65_.jpg?text=Sneakers',
            'Watch': 'https://m.media-amazon.com/images/I/512sO2L0k6L._AC_UL640_FMwebp_QL65_.jpg?text=Watch',
            'Handbag': 'https://m.media-amazon.com/images/I/512sO2L0k6L._AC_UL640_FMwebp_QL65_.jpg?text=Handbag',
            'Sunglasses': 'https://m.media-amazon.com/images/I/512sO2L0k6L._AC_UL640_FMwebp_QL65_.jpg?text=Sunglasses',
            'Hat': 'https://m.media-amazon.com/images/I/512sO2L0k6L._AC_UL640_FMwebp_QL65_.jpg?text=Hat',
            'Dress': 'https://m.media-amazon.com/images/I/512sO2L0k6L._AC_UL640_FMwebp_QL65_.jpg?text=Dress',
            'Boots': 'https://m.media-amazon.com/images/I/512sO2L0k6L._AC_UL640_FMwebp_QL65_.jpg?text=Boots',

            # Home
            'Sofa': 'https://m.media-amazon.com/images/I/512sO2L0k6L._AC_UL640_FMwebp_QL65_.jpg?text=Sofa',
            'Lamp': 'https://m.media-amazon.com/images/I/512sO2L0k6L._AC_UL640_FMwebp_QL65_.jpg?text=Lamp',
            'Chair': 'https://m.media-amazon.com/images/I/512sO2L0k6L._AC_UL640_FMwebp_QL65_.jpg?text=Chair',
            'Table': 'https://m.media-amazon.com/images/I/512sO2L0k6L._AC_UL640_FMwebp_QL65_.jpg?text=Table',
            'Rug': 'https://m.media-amazon.com/images/I/512sO2L0k6L._AC_UL640_FMwebp_QL65_.jpg?text=Rug',
            'Curtains': 'https://m.media-amazon.com/images/I/512sO2L0k6L._AC_UL640_FMwebp_QL65_.jpg?text=Curtains',
            'Cushion': 'https://m.media-amazon.com/images/I/512sO2L0k6L._AC_UL640_FMwebp_QL65_.jpg?text=Cushion',
            'Bookshelf': 'https://m.media-amazon.com/images/I/512sO2L0k6L._AC_UL640_FMwebp_QL65_.jpg?text=Bookshelf',
            'Vase': 'https://m.media-amazon.com/images/I/512sO2L0k6L._AC_UL640_FMwebp_QL65_.jpg?text=Vase',
            'Planter': 'https://m.media-amazon.com/images/I/512sO2L0k6L._AC_UL640_FMwebp_QL65_.jpg?text=Planter',

            # Books
            'Novel': 'https://m.media-amazon.com/images/I/512sO2L0k6L._AC_UL640_FMwebp_QL65_.jpg?text=Novel',
            'Biography': 'https://m.media-amazon.com/images/I/512sO2L0k6L._AC_UL640_FMwebp_QL65_.jpg?text=Biography',
            'Cookbook': 'https://m.media-amazon.com/images/I/512sO2L0k6L._AC_UL640_FMwebp_QL65_.jpg?text=Cookbook',
            'Sci-Fi': 'https://m.media-amazon.com/images/I/512sO2L0k6L._AC_UL640_FMwebp_QL65_.jpg?text=Sci-Fi',
            'History': 'https://m.media-amazon.com/images/I/512sO2L0k6L._AC_UL640_FMwebp_QL65_.jpg?text=History',
            'Thriller': 'https://m.media-amazon.com/images/I/512sO2L0k6L._AC_UL640_FMwebp_QL65_.jpg?text=Thriller',
            'Guide': 'https://m.media-amazon.com/images/I/512sO2L0k6L._AC_UL640_FMwebp_QL65_.jpg?text=Guide',
            'Art Book': 'https://m.media-amazon.com/images/I/512sO2L0k6L._AC_UL640_FMwebp_QL65_.jpg?text=Art+Book',
            'Comic': 'https://m.media-amazon.com/images/I/512sO2L0k6L._AC_UL640_FMwebp_QL65_.jpg?text=Comic',
            'Dictionary': 'https://m.media-amazon.com/images/I/512sO2L0k6L._AC_UL640_FMwebp_QL65_.jpg?text=Dictionary',
        }
        
        fallback_url = "https://m.media-amazon.com/images/I/512sO2L0k6L._AC_UL640_FMwebp_QL65_.jpg"

        for cat_name, items in categories_data.items():
            category = Category.objects.create(name=cat_name, slug=slugify(cat_name))
            self.stdout.write(f'Created category: {cat_name}')
            
            # Select 6 random items per category
            selected_items = random.sample(items, 6)
            
            for item in selected_items:
                adj = random.choice(adjectives)
                prod_name = f'{adj} {item}'
                slug = slugify(f"{prod_name}-{random.randint(1000, 9999)}")
                price = round(random.uniform(10.0, 999.0), 2)
                
                description = (
                    f"This is a fantastic {prod_name}. It features top-notch quality, "
                    f"elegant design, and is perfect for your needs. "
                    f"One of our best-selling items in the {cat_name} category."
                )

                product = Product(
                    category=category,
                    name=prod_name,
                    slug=slug,
                    description=description,
                    price=price,
                    available=True
                )

                try:
                    # Get specific URL from map or fallback
                    image_url = item_image_mappings.get(item, fallback_url)
                    
                    # Set a timeout (10 seconds)
                    response = urllib.request.urlopen(image_url, timeout=10)
                    if response.status == 200:
                        image_name = f"{slug}.jpg"
                        product.image.save(image_name, ContentFile(response.read()), save=False)
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'Failed to download image for {prod_name}: {e}'))

                product.save()
                self.stdout.write(f'  - Added: {prod_name}')
        
        self.stdout.write(self.style.SUCCESS('Successfully populated database with diverse sample data and images'))
