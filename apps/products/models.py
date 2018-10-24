from django.db import models
from apps.users.models import User

STATUS_PRODUCT = (("available", "Available"), ("requested_not_confirmed", "Solicitado"), ("requested_confirmed", "Solicitado"), ("requested_deliver", "No disponible"))

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, choices=STATUS_PRODUCT, default="available")
    updated_at = models.DateTimeField()


class Image(models.Model):
    file = models.ImageField(upload_to="product_images/")


class ImageProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)


class ReportProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
