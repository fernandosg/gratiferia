from django.db import models
from custom_user.models import AbstractEmailUser

# Create your models here.
class User(AbstractEmailUser):
    name = models.CharField(max_length=100)
    first_last_name = models.CharField(max_length=100)
    second_last_name = models.CharField(max_length=100)
