from django.urls import path
from . import api_views

urlpatterns = [
    # Product
    path("products/", api_views.product_list),
    path("products/<int:pk>/", api_views.product_detail),

    # Category
    path("categories/", api_views.category_list),
    path("categories/<int:pk>/", api_views.category_detail),

    # Order
    path("orders/", api_views.order_list),
    path("orders/<int:pk>/", api_views.order_detail),

    # OrderItem
    path('order-items/', api_views.order_item_list),
    path('order-items/<int:pk>/', api_views.order_item_detail),

    path(
    "register/",
    api_views.register_api,
    name="register_api"),

    path(
    "login/",
    api_views.login_api,
    name="login_api"),

    path(
    "logout/",
    api_views.logout_api,
    name="logout_api"),

    path(
    "shipping-addresses/",
    api_views.shipping_address_list,
    name="shipping_address_list"),

    path(
    "shipping-addresses/<int:pk>/",
    api_views.shipping_address_detail,
    name="shipping_address_detail"),
]