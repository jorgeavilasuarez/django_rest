from django.db import models


class Order(models.Model):
    order_id = models.AutoField(primary_key=True, blank=True)
    customer_id = models.IntegerField(blank=True, null=True)
    creation_date = models.DateField(auto_created=True)
    delivery_address = models.TextField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order'


class OrderDetail(models.Model):
    order_detail_id = models.AutoField(primary_key=True, blank=True)
    product_description = models.TextField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    order_id = models.IntegerField(blank=True, null=True)
    product_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order_detail'


class Product(models.Model):
    product_id = models.AutoField(primary_key=True, blank=True)
    name = models.TextField(blank=True, null=True)
    product_description = models.TextField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product'


class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True, blank=True)
    name = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customer'


class CustomerProduct(models.Model):
    customer_product_id = models.AutoField(primary_key=True, blank=True)
    customer_id = models.IntegerField(blank=True, null=True)
    product_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customer_product'


class OrderRequest:
    customer_id = models.IntegerField(blank=True, null=True)
    product_id = models.IntegerField(blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
