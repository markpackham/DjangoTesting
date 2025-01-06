from django.test import TestCase
from django.contrib.auth.models import AbstractUser

# Create your tests here.
class User(AbstractUser):
    pass

class Product(models.Model):
    name = models.CharField(max_length=128)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_count = models.IntegerField(default=0)
