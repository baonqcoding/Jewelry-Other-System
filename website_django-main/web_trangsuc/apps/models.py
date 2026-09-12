from django.db import models # type: ignore
from django.contrib.auth.models import User # type: ignore
from django.contrib.auth.forms import UserCreationForm # type: ignore
from django.core.validators import MinValueValidator, RegexValidator
from django import forms # type: ignore

from .auth_bounds import (
    USERNAME_MIN_LENGTH,
    USERNAME_MAX_LENGTH,
    PASSWORD_MIN_LENGTH,
    PASSWORD_MAX_LENGTH,
    EMAIL_MIN_LENGTH,
    EMAIL_MAX_LENGTH,
    FIRST_NAME_MAX_LENGTH,
    LAST_NAME_MAX_LENGTH,
)

# Create your models here.
#change forms register django
class Category(models.Model):
    sub_category =models.ForeignKey('self', on_delete=models.CASCADE, related_name ='sub_categories', null =True, blank =True)
    is_sub =models.BooleanField(default=False)
    name = models.CharField(max_length = 200, null =True)
    slug =models.SlugField(max_length=200, unique=True)
    def __str__(self):
        return self.name
class CreateUserForm(UserCreationForm):
    """Web register — cung boundary voi API (auth_bounds)."""
    username = forms.CharField(
        min_length=USERNAME_MIN_LENGTH,
        max_length=USERNAME_MAX_LENGTH,
        validators=[
            RegexValidator(
                regex=r"^[A-Za-z0-9_]+$",
                message="Username may only contain letters, numbers, and underscore",
            )
        ],
    )
    email = forms.EmailField(
        min_length=EMAIL_MIN_LENGTH,
        max_length=EMAIL_MAX_LENGTH,
    )
    first_name = forms.CharField(required=False, max_length=FIRST_NAME_MAX_LENGTH)
    last_name = forms.CharField(required=False, max_length=LAST_NAME_MAX_LENGTH)
    password1 = forms.CharField(
        min_length=PASSWORD_MIN_LENGTH,
        max_length=PASSWORD_MAX_LENGTH,
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        min_length=PASSWORD_MIN_LENGTH,
        max_length=PASSWORD_MAX_LENGTH,
        widget=forms.PasswordInput,
    )

    class Meta:
        model =User
        fields =['username', 'email','first_name', 'last_name', 'password1', 'password2']
class Product(models.Model):
    category = models.ManyToManyField(Category, related_name='product')
    name = models.CharField(max_length=200, null=True)
    price = models.IntegerField(validators=[MinValueValidator(0)])
    detail =models.TextField(null=True, blank = True)
    # digital = models .BooleanField(default=False, null = True, blank = False)
    image = models.ImageField(null =True, blank = True)
    def __str__(self):
        return self.name
    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    date_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null= True, blank = True)
    transaction_id = models.CharField(max_length=200, null = True)
    def __str__(self):
        return str(self.id)
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,blank = True, null = True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL,blank = True, null = True)
    quantity = models.IntegerField(default=0, null = True, blank= True)
    date_added = models.DateTimeField(auto_now_add=True)
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    
class ShippingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL,blank = True, null = True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL,blank = True, null = True)
    address = models.CharField(max_length=200, null = True)
    city  = models.CharField(max_length=200, null = True)
    state = models.CharField(max_length=200, null = True)
    mobile = models.CharField(max_length=10, null = True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.address)
    
