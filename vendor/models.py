from django.db import models
# from django.contrib.auth.models import User
from users.models import CustomUser as User

# Create your models here.


class Vendor(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
