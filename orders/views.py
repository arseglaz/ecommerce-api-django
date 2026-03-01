from django.shortcuts import render

from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Order, OrderItem
from .serializers import OrderSerializer
from cart.models import Cart, CartItem


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items__product')

    @action(detail=False, methods=['post'], url_path='create_from_cart')
    def create_from_cart(self, request):
        user = request.user
        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            return Response(
                {'error': 'Cart is empty.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart_items = cart.items.select_related('product')
        if not cart_items.exists():
            return Response(
                {'error': 'Cart has no items.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        
        with transaction.atomic():
            total_price = sum(item.subtotal for item in cart_items)

            order = Order.objects.create(
                user=user,
                total_price=total_price,
            )

            order_items = []
            for item in cart_items:
                order_items.append(OrderItem(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price,  
                ))
                
                if item.product.stock_quantity >= item.quantity:
                    item.product.stock_quantity -= item.quantity
                    item.product.save()
                

            OrderItem.objects.bulk_create(order_items)

            
            cart.items.all().delete()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

