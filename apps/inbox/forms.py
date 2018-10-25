from django.forms import ModelForm
from .models import *


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ("content",)


class ResponseMessageForm(ModelForm):
    class Meta:
        model = ResponseMessage
        fields = ("content",)
