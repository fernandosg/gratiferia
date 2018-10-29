from django.urls import path
from .views import *

urlpatterns = [
    path("revition/", RevitionIndexView.as_view(), name="revition_index"),
    path("revition/products/", RevitionProductIndexView.as_view(), name="revition_product_index"),
    path("revition/images/", RevitionImageIndexView.as_view(), name="revition_image_index"),
    path("events/", EventsDashboardView.as_view(), name="events_index_dashboard"),
    path("events/create/", EventsDashboardCreateView.as_view(), name="events_create_dashboard"),
    path("events/<int:id>/", EventsDashboardEditView.as_view(), name="events_edit_dashboard"),
]
