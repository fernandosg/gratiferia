from django.urls import path
from .views import *

urlpatterns = [
    path("", ProductIndexView.as_view(), name="product_index"),
    path("category/<slug:slug>", ProductsByCategoryView.as_view(), name="products_by_category"),
    path("create/", ProductCreateView.as_view(), name="product_create"),
    path("<slug:slug>/", ProductDetailView.as_view(), name="product_detail"),
    path("<slug:slug>/edit", ProductEditView.as_view(), name="product_edit"),
    path("<slug:slug>/request", ProductRequestView.as_view(), name="product_request"),
    path("<slug:slug>/images/create", ProductImageCreateView.as_view(), name="product_image_create"),
]
