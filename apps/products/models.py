from django.db import models
from apps.users.models import User
from django.utils.text import slugify

STATUS_PRODUCT = (("available", "Available"), ("requested_not_confirmed", "Solicitado"), ("requested_confirmed", "Solicitado"), ("requested_deliver", "No disponible"))

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, blank=True, null=True, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        

class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=100, blank=True, null=True, unique=True)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    contact = models.TextField(verbose_name="Datos de contacto. Puedes escribir una dirección incluyendo número telefónico, o solo el número telefónico. Esta información será visible y se le enviara a la persona que hayas aceptado entregarle el producto.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, choices=STATUS_PRODUCT, default="available")
    visible = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def is_not_available(self):
        return self.status != "available"

    def confirm_deliver(self):
        self.status = "requested_confirmed"
        self.save()

    def request_product(self):
        if self.status == "available":
            self.status = "requested_not_confirmed"
            self.save()

    def confirm_received(self):
        self.status = "requested_deliver"
        self.save()

    def set_available(self):
        self.status = 'available'
        self.save()

class Image(models.Model):
    file = models.ImageField(upload_to="product_images/")


class ImageProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_images")
    image = models.ForeignKey(Image, on_delete=models.CASCADE)


class ReportProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    reviewed = models.BooleanField(default=False)


class RequestProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="requests_product")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="requests_users")
    is_cancel = models.BooleanField(default=False)

    def cancel(self):
        self.is_cancel = True
        self.product.set_available()
        self.save()
