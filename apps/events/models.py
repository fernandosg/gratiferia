from django.db import models
from datetime import datetime

# Create your models here.
class Event(models.Model):
    description = models.TextField()
    date_event = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    address = models.TextField()
    flyer = models.ImageField(upload_to="event_flyer", default='/placeholder.gif')

    def last_event(self):
        return Event.objects.filter(date_event__gte=datetime.now()).first()

    @property
    def date_event_display(self):
        return self.date_event.strftime("%d %b")

    @property
    def get_date(self):
        return self.date_event.strftime("%d %M %y")

    @property
    def get_hour(self):
        return self.date_event.strftime("%H:%M")
