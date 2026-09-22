from django.contrib.auth.models import User
from apps.models import Category, Product, Order, OrderItem, ShippingAddress


def make_user(username="user1", password="Passw0rd!", **kwargs):
    return User.objects.create_user(
        username=username,
        password=password,
        email=kwargs.get("email", f"{username}@example.com"),
        first_name=kwargs.get("first_name", "Van"),
        last_name=kwargs.get("last_name", "A"),
    )


def make_category(**kwargs):
    data = {"name": "Nhan", "slug": "nhan", "is_sub": False}
    data.update(kwargs)
    return Category.objects.create(**data)


def make_product(**kwargs):
    data = {"name": "Nhan kim cuong", "price": 1_000_000, "detail": "18K"}
    data.update(kwargs)
    return Product.objects.create(**data)


def make_order(user=None, **kwargs):
    data = {"customer": user, "complete": False}
    data.update(kwargs)
    return Order.objects.create(**data)


def make_order_item(order, product, quantity=1):
    return OrderItem.objects.create(order=order, product=product, quantity=quantity)


def make_shipping(user, order, **kwargs):
    data = {
        "customer": user,
        "order": order,
        "address": "123 Nguyen Trai",
        "city": "Ha Noi",
        "state": "Ha Noi",
        "mobile": "0912345678",
    }
    data.update(kwargs)
    return ShippingAddress.objects.create(**data)
