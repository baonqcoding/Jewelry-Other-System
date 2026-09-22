from rest_framework import serializers
from .models import (
    Product,
    Category,
    Order,
    OrderItem,
    ShippingAddress
)
from django.contrib.auth.models import User
from .domain_bounds import (
    validate_category_fields,
    validate_order_fields,
    validate_product_fields,
    validate_shipping_fields,
)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        extra_kwargs = {
            "category": {"required": False},
            "name": {"allow_blank": True, "required": False},
            "detail": {"required": False, "allow_blank": True},
        }

    def validate(self, attrs):
        # merge instance values for PUT-style full update checks via attrs only
        data = {**attrs}
        # ModelSerializer already ran field-level; add domain BVA rules
        payload = {
            "name": data.get("name", getattr(self.instance, "name", None)),
            "price": data.get("price", getattr(self.instance, "price", None)),
            "detail": data.get("detail", getattr(self.instance, "detail", None)),
        }
        # For create, name/price must be in attrs
        partial = self.partial
        check = {}
        if "name" in attrs or not partial:
            check["name"] = attrs.get("name") if "name" in attrs else payload["name"]
        if "price" in attrs or not partial:
            check["price"] = attrs.get("price") if "price" in attrs else payload["price"]
        if "detail" in attrs:
            check["detail"] = attrs.get("detail")

        # On create (no instance): require name+price
        if self.instance is None:
            check = {
                "name": attrs.get("name"),
                "price": attrs.get("price"),
                "detail": attrs.get("detail"),
            }
            errors = validate_product_fields(check, partial=False)
        else:
            # PUT sends full body via API views (not partial)
            check = {
                "name": attrs.get("name", self.instance.name),
                "price": attrs.get("price", self.instance.price),
                "detail": attrs.get("detail", self.instance.detail),
            }
            errors = validate_product_fields(check, partial=False)

        if errors:
            raise serializers.ValidationError({"error": errors[0], "errors": errors})
        return attrs


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        extra_kwargs = {
            "name": {"allow_blank": True, "required": False},
            "slug": {"allow_blank": True, "required": False},
        }

    def validate(self, attrs):
        if self.instance is None:
            check = {
                "name": attrs.get("name"),
                "slug": attrs.get("slug"),
                "is_sub": attrs.get("is_sub"),
            }
        else:
            check = {
                "name": attrs.get("name", self.instance.name),
                "slug": attrs.get("slug", self.instance.slug),
                "is_sub": attrs.get("is_sub", self.instance.is_sub),
            }
        errors = validate_category_fields(check, partial=False)
        if errors:
            raise serializers.ValidationError({"error": errors[0], "errors": errors})
        return attrs


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"

    def validate(self, attrs):
        check = dict(attrs)
        if self.instance is not None and "transaction_id" not in attrs:
            check["transaction_id"] = self.instance.transaction_id
        errors = validate_order_fields(check, partial=self.partial)
        if errors:
            raise serializers.ValidationError({"error": errors[0], "errors": errors})
        return attrs


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
        extra_kwargs = {
            "address": {"allow_blank": True, "required": False},
            "city": {"allow_blank": True, "required": False},
            "state": {"required": False, "allow_blank": True},
            "mobile": {"allow_blank": True, "required": False},
        }

    def validate(self, attrs):
        if self.instance is None:
            check = {
                "address": attrs.get("address"),
                "city": attrs.get("city"),
                "state": attrs.get("state"),
                "mobile": attrs.get("mobile"),
            }
        else:
            check = {
                "address": attrs.get("address", self.instance.address),
                "city": attrs.get("city", self.instance.city),
                "state": attrs.get("state", self.instance.state),
                "mobile": attrs.get("mobile", self.instance.mobile),
            }
        errors = validate_shipping_fields(check, partial=False)
        if errors:
            raise serializers.ValidationError({"error": errors[0], "errors": errors})
        return attrs
