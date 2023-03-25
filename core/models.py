from django.db import models
# from django.contrib.auth.models import User
from users.models import CustomUser as User

# Create your models here.
from vendor.models import Vendor

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.CharField(max_length=10, blank=True, null=True)
    quantity = models.IntegerField()
    image = models.ImageField(upload_to='pictures/')
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE,null=True,blank=True)
    quantity = models.IntegerField()
    number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    processed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name