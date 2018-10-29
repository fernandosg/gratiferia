from django.db import models

# Create your models here.
class Event(models.Model):
    description = models.TextField()
    date_event = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
