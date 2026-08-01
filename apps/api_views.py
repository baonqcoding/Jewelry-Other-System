from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Product, Category, Order, OrderItem, ShippingAddress
from .serializers import (
    ProductSerializer,
    CategorySerializer,
    OrderSerializer,
    OrderItemSerializer,
    UserSerializer,
    ShippingAddressSerializer
)

@api_view(['GET', 'POST'])
def product_list(request):

    # GET: Lấy danh sách sản phẩm
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    # POST: Thêm sản phẩm mới
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)

@api_view(['GET', 'POST'])
def category_list(request):

    # GET: Lấy tất cả category
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    # POST: Thêm category mới
    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def category_detail(request, pk):

    try:
        category = Category.objects.get(id=pk)
    except Category.DoesNotExist:
        return Response(
            {"error": "Category not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    # GET
    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    # PUT
    elif request.method == 'PUT':
        serializer = CategorySerializer(
            category,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # DELETE
    elif request.method == 'DELETE':
        category.delete()

        return Response(
            {"message": "Category deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )

@api_view(['GET', 'POST'])
def order_list(request):

    # GET: Lấy tất cả đơn hàng
    if request.method == 'GET':

        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)

        return Response(serializer.data)

    # POST: Tạo đơn hàng mới
    elif request.method == 'POST':

        serializer = OrderSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['GET'])
def order_item_list(request):

    order_items = OrderItem.objects.all()
    serializer = OrderItemSerializer(order_items, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def order_item_detail(request, pk):

    try:
        order_item = OrderItem.objects.get(id=pk)
    except OrderItem.DoesNotExist:
        return Response(
            {"error": "OrderItem not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = OrderItemSerializer(order_item)
    return Response(serializer.data)

@api_view(['GET', 'PUT', 'DELETE'])
def order_detail(request, pk):

    try:
        order = Order.objects.get(id=pk)

    except Order.DoesNotExist:
        return Response(
            {"error": "Order not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    # GET
    if request.method == 'GET':

        serializer = OrderSerializer(order)

        return Response(serializer.data)

    # PUT
    elif request.method == 'PUT':

        serializer = OrderSerializer(
            order,
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # DELETE
    elif request.method == 'DELETE':

        order.delete()

        return Response(
            {
                "message": "Order deleted successfully"
            },
            status=status.HTTP_204_NO_CONTENT
        )
    
@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, pk):

    try:
        product = Product.objects.get(id=pk)
    except Product.DoesNotExist:
        return Response(
            {"error": "Product not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    # GET
    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    # PUT
    elif request.method == 'PUT':
        serializer = ProductSerializer(
            product,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # DELETE
    elif request.method == 'DELETE':
        product.delete()

        return Response(
            {"message": "Product deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )


@api_view(['POST'])
def register_api(request):

    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")
    first_name = request.data.get("first_name")
    last_name = request.data.get("last_name")

    # Kiểm tra username đã tồn tại
    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "Username already exists"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Tạo user
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name
    )

    serializer = UserSerializer(user)

    return Response(
        serializer.data,
        status=status.HTTP_201_CREATED
    )

@api_view(['POST'])
def login_api(request):

    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(
        request,
        username=username,
        password=password
    )

    if user is not None:
        login(request, user)

        serializer = UserSerializer(user)

        return Response(
            {
                "message": "Login successful",
                "user": serializer.data
            },
            status=status.HTTP_200_OK
        )

    return Response(
        {
            "error": "Invalid username or password"
        },
        status=status.HTTP_401_UNAUTHORIZED
    )

@api_view(['POST'])
def logout_api(request):

    logout(request)

    return Response(
        {
            "message": "Logout successful"
        },
        status=status.HTTP_200_OK
    )

@api_view(['GET', 'POST'])
def shipping_address_list(request):

    # GET: Lấy tất cả địa chỉ giao hàng
    if request.method == 'GET':

        addresses = ShippingAddress.objects.all()
        serializer = ShippingAddressSerializer(addresses, many=True)

        return Response(serializer.data)

    # POST: Thêm địa chỉ giao hàng mới
    elif request.method == 'POST':

        serializer = ShippingAddressSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['GET', 'PUT', 'DELETE'])
def shipping_address_detail(request, pk):

    try:
        shipping_address = ShippingAddress.objects.get(id=pk)

    except ShippingAddress.DoesNotExist:
        return Response(
            {"error": "Shipping address not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    # GET
    if request.method == 'GET':

        serializer = ShippingAddressSerializer(shipping_address)

        return Response(serializer.data)

    # PUT
    elif request.method == 'PUT':

        serializer = ShippingAddressSerializer(
            shipping_address,
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # DELETE
    elif request.method == 'DELETE':

        shipping_address.delete()

        return Response(
            {
                "message": "Shipping address deleted successfully"
            },
            status=status.HTTP_204_NO_CONTENT
        )