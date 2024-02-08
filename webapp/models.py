from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'manager'),
        ('operator', 'operator'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=100, choices=ROLE_CHOICES) 
    
    def __str__(self):
        return str(self.user)

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    pic = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Tag(models.Model):
    tag_item = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.tag_item
   
class Product(models.Model):
    category = models.CharField(max_length=100)
    product_sku = models.CharField(max_length=100, unique=True)
    product_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    quantity = models.IntegerField()
    remarks = models.CharField(max_length=100)
    tags = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return(f"{self.product_sku}{self.product_name}")
    
class Inbound_Product(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    quantity_received = models.IntegerField()
    tags = models.CharField(max_length=100)  #
    remarks = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return(f"{self.product.product_sku} {self.product.product_name}")

class Outbound_Product(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity_sold = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return(f"{self.outbound_id} {self.product_name}")   
