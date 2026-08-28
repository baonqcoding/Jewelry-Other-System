from django.urls import path # type: ignore
from . import api_views, views

urlpatterns = [
    path('', views.home, name='home'),  # Trang chủ
    path('product/', views.show_products, name='product'),  # Sản phẩm
    path('cart/', views.cart, name='cart'),  # Giỏ hàng
    path('contact/', views.contact, name='contact'),  # Liên hệ
    path('payment/', views.payment, name='payment'),  # thanh toán
    path('update_item/', views.updateItem, name='update_item'),  # 
    path('register/', views.register, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('search/', views.search, name='search'),
    path('category/', views.category, name='category'),
    path('detail/', views.detail, name='detail'),
    path('api/products/<int:pk>/reviews/', api_views.product_reviews_api, name='product_reviews_api'),
    path('api/wishlist/', api_views.wishlist_api, name='wishlist_api'),
]
