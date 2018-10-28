from django.test import TestCase
from apps.products.models import Product, Category
from apps.users.models import User

# Create your tests here.
class RequestProductTest(TestCase):

    def setUp(self):
        User.objects.create(email="test@gratiferia.com", password="testgratiferia")
        Category.objects.create(name="test")

    def test_request_product_success(self):
        user = User.objects.first()
        product = Product.objects.create(name="Test product", author=user, contact="X", category=Category.objects.first())
        product.request_product()
        self.assertTrue(product.is_not_available())
