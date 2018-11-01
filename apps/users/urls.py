from django.urls import path
from .views import ProfileView, UserProductsView

urlpatterns = [
    path("<int:user_id>/", ProfileView.as_view(), name="profile_view"),
    path("<int:user_id>/products", UserProductsView.as_view(), name="user_products"),
]
