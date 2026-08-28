from rest_framework import serializers
from .models import (
    Product,
    Category,
    Order,
    OrderItem,
    ShippingAddress,
    Wishlist,
    Review,
)
from django.contrib.auth.models import User


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"       


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"         


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
        ]

class ShippingAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShippingAddress
        fields = "__all__"               


class WishlistSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    price = serializers.ReadOnlyField(source='product.price')

    class Meta:
        model = Wishlist
        fields = ['id', 'customer', 'product', 'product_name', 'price', 'date_added']

class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='customer.username')

    class Meta:
        model = Review
        fields = ['id', 'product', 'customer', 'username', 'rating', 'comment', 'date_added']