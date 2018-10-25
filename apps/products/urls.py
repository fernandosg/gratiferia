from django.urls import path
from .views import *

urlpatterns = [
    path("create/", ProductCreateView.as_view(), name="product_create"),
    path("<slug:slug>/", ProductDetailView.as_view(), name="product_detail"),
    path("<slug:slug>/edit", ProductEditView.as_view(), name="product_edit"),
]
