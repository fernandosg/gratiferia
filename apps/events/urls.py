from django.urls import path
from .views import *

urlpatterns = [
    path("", EventListView.as_view(), name="events_list"),
    path("<int:id>/", EventDetailView.as_view(), name="event_detail"),
]
