from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from apps.inbox.models import Message, ResponseMessage
from apps.inbox.forms import MessageForm, ResponseMessageForm
from apps.users.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.
class InboxIndexView(View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        messages = ResponseMessage.objects.filter(to_user=request.user).order_by("created_at").all()
        return render(request, "panel/inbox/index.html", locals())


class MessageDetailView(View):

    @property
    def id(self):
        if "id" in self.kwargs:
            return self.kwargs["id"]
        return None

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        message = Message.objects.filter(id=self.id).first()
        return render(request, "panel/inbox/detail.html", locals())

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        post = request.POST.copy()
        form = ResponseMessageForm(post)
        message = Message.objects.filter(id=self.id).first()
        if form.is_valid():
            response_message = form.save(commit=False)
            response_message.from_user = request.user
            response_message.to_user = (message.to_user if message.to_user.id != request.user.id else message.from_user)
            response_message.parent_message = message
            response_message.save()
        else:
            for e in form.errors:
                message.error(request, e)
        return render(request, "panel/inbox/detail.html", locals())


class MessageCreateView(View):

    @property
    def user(self):
        if "user" in self.kwargs:
            return self.kwargs["user"]
        return None

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        to_user = self.user
        return render(request, "panel/inbox/create.html", locals())

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        post = request.POST.copy()
        form = MessageForm(post)
        if form.is_valid():
            message = form.save(commit=False)
            message.to_user = User.objects.filter(id=post["to_user"]).first()
            message.from_user = request.user
            message.save()
            return redirect(reverse("inbox_index"))
        else:
            for e in form.errors:
                print(e)
                messages.error(request, e)
        return render(request, "panel/inbox/create.html", locals())
