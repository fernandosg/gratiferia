from django.db import models
from datetime import datetime

# Create your models here.
class Event(models.Model):
    description = models.TextField()
    date_event = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    address = models.TextField()

    def last_event(self):
        return Event.objects.filter(date_event__gte=datetime.now()).first()
