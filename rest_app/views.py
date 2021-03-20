from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, OrderDetail, Order, Customer, CustomerProduct
from .serializer import ProductSerializer, OrderDetailSerializer, OrderSerializer, CustomerSerializer,\
    CustomerProductSerializer, OrderRequestSerializer
import datetime


def get_orders(customer_id, date_ini, date_end):
    """
     Get orders 
     Args: customer_id 
        date_ini 
        date_end
    """
    orders = Order.objects.filter(
        customer_id=customer_id,
        creation_date__range=(date_ini, date_end))
    serializer_orders = OrderSerializer(orders, many=True)

    order_ids = [order.order_id for order in orders]
    order_details = OrderDetail.objects.filter(order_id__in=order_ids)
    serializer_order_details =\
        OrderDetailSerializer(order_details, many=True)

    product_ids = [order_detail.product_id for order_detail in order_details]
    products = Product.objects.filter(product_id__in=product_ids)
    serializer_products = ProductSerializer(products, many=True)

    customer_ids = [order.customer_id for order in orders]
    customers = Customer.objects.filter(customer_id__in=customer_ids)
    serializer_customer = CustomerSerializer(customers, many=True)

    return {"customer": serializer_customer.data,
            "order": serializer_orders.data,
            "order_details": serializer_order_details.data,
            "products": serializer_products.data}


@api_view(['GET', 'POST'])
def orders_list(request):
    """
    List all orders by range of dates
    """
    if request.method == 'GET':
        customer_id = request.GET.get("customer_id")
        date_ini = request.GET.get("date_ini")
        date_end = request.GET.get("date_end")
        orders = get_orders(customer_id, date_ini, date_end)
        return Response(orders)

    elif request.method == 'POST':
        customer_id = request.data.get("customer_id")
        delivery_address = request.data.get("delivery_address")
        total = request.data.get("total")
        order = Order.objects.create(creation_date=datetime.datetime.now(),
                                     delivery_address=delivery_address,
                                     customer_id=customer_id,
                                     total=total)
        order.save()
        for product in request.data.get("product_list"):
            order_detail = OrderDetail.objects.create(
                product_description=product.get('product_description'),
                order_id=order.order_id,
                price=product.get('price'),
                quantity=product.get('quantity'),
                product_id=product.get('product_id'))
            order_detail.save()

        return Response({'result': 'ok'}, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def customer_list(request):
    """
    List all orders by range of dates
    """
    if request.method == 'GET':
        customer = Customer.objects.all()
        serializer_customer = CustomerSerializer(customer, many=True)

        products = Product.objects.all()
        serializer_products = ProductSerializer(products, many=True)

        customer_product = CustomerProduct.objects.all()
        serializer_customer_product = CustomerProductSerializer(
            customer_product, many=True)

        return Response({"customer": serializer_customer.data,
                         "customer_product": serializer_customer_product.data,
                         "products": serializer_products.data})


def index(request):
    return render(request, 'index.html')
