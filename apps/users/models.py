from django.db import models
from custom_user.models import AbstractEmailUser

# Create your models here.
class User(AbstractEmailUser):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    first_last_name = models.CharField(max_length=100, verbose_name="Apellido paterno")
    second_last_name = models.CharField(max_length=100, verbose_name="Apellido materno")
