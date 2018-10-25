from django.db import models
from apps.users.models import User

# Create your models here.
class Message(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="from_user_message")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to_user_message")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    open = models.BooleanField(default=False)

    def is_open(self, user):
        return user.id != self.to_user.id and self.open

    def open_message(self, user):
        if user.id == self.to_user.id:
            self.open = True
            self.save()

class ResponseMessage(models.Model):
    parent_message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="parent_message")
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="from_user_response_message")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to_user_response_message")
    open = models.BooleanField(default=False)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def is_open(self, user):
        return user.id != self.to_user.id and self.open

    def open_message(self, user):
        if user.id == self.to_user.id:
            self.open = True
            self.save()
