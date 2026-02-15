from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'products_count', 'created_at']
        read_only_fields = ['slug', 'created_at']
    
    def get_products_count(self, obj):
        return obj.products.count()


class ProductListSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'category', 'price', 'is_in_stock', 'image']


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 
            'category', 'category_id',
            'price', 'stock_quantity', 'is_in_stock',
            'image', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['slug', 'created_at', 'updated_at', 'is_in_stock']
