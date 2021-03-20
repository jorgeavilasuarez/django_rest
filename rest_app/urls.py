from django.urls import path

from . import views

urlpatterns = [
    path('customers/', views.customer_list),
    path('orders/', views.orders_list),
    path('', views.index, name='index'),
]
