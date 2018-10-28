from django.urls import path
from .views import *

urlpatterns = [
    path("revition/", RevitionIndexView.as_view(), name="revition_index"),
    path("revition/products/", RevitionProductIndexView.as_view(), name="revition_product_index"),
    path("revition/images/", RevitionImageIndexView.as_view(), name="revition_image_index")
]
