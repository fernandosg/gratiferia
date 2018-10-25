from django.urls import path
from .views import *

urlpatterns = [
    path("inbox/", InboxIndexView.as_view(), name="inbox_index"),
    path("inbox/<int:id>/", MessageDetailView.as_view(), name="inbox_detail"),
    path("inbox/create/<int:user>", MessageCreateView.as_view(), name="inbox_create"),
]
