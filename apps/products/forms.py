from django.forms import ModelForm
from .models import *

class ProductForm(ModelForm):
    class Meta:
        model = Product
        exclude = ('status', 'created_at', 'updated_at', 'author', 'slug')

class ImageForm(ModelForm):
    class Meta:
        model = Image
        exclude = ("",)
