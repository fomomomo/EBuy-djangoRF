from rest_framework import serializers
from .models import *

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'imageURL']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['date_ordered', 'complete', 'customer', 'transaction_id', 'get_cart_total', 'get_cart_items']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product_id', 'order', 'product_name', 'quantity', 'date_added', 'product_price', 'imageURL']
    
class AddOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['order', 'product', 'quantity']

