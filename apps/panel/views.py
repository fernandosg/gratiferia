from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.http import HttpResponseForbidden
from apps.inbox.models import Message, ResponseMessage
from apps.inbox.forms import MessageForm, ResponseMessageForm
from apps.users.models import User
from apps.products.models import Product, RequestProduct
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.
class InboxIndexView(View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        messages = ResponseMessage.objects.filter(to_user=request.user).order_by("created_at").all()
        option = "received"
        return render(request, "panel/inbox/index.html", locals())


class InboxSendView(View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        messages = Message.objects.filter(from_user=request.user).order_by("created_at").all()
        option = "send"
        return render(request, "panel/inbox/send.html", locals())

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


class RequestsProductReceivedView(View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        requests_product = RequestProduct.objects.filter(product__author__id=request.user.id).all()
        requests_product_made = RequestProduct.objects.filter(user__id=request.user.id).all()
        title = "Solicitudes de productos"
        return render(request, "panel/requests/received.html", locals())


class RequestsProductDetailView(View):

    @property
    def id(self):
        if "id" in self.kwargs:
            return self.kwargs["id"]
        return None


    def send_message_from_author_for_request_confirmed(self, user_request, contact_product):
        content = "Hola {}, he visto tu solicitud y te confirmo la posibilidad de ponernos en contacto. Por favor, ponte en contacto conmigo por los siguientes medios: {}.".format(user_request.name, contact_product)
        Message.objects.create(from_user=self.request.user, to_user=user_request, content=content)

    def send_message_to_author_for_product_received_confirmed(self, author_product):
        content = "Hola {}, confirmo la recepción del producto, el cual ya no podrá ser solicitado por otra persona. Gracias por hacer entrega del producto.".format(author_product)
        Message.objects.create(from_user=self.request.user, to_user=author_product, content=content)

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        request_product = RequestProduct.objects.filter(id=self.id).first()
        title = "Detalle de la solicitud del producto {}".format(request_product.product.name)
        if request_product.user.id != request.user.id and request_product.product.author.id != request.user.id or request_product.is_cancel:
            return HttpResponseForbidden()
        return render(request, "panel/requests/detail.html", locals())

    def _confirm_deliver(self, post, request_product):
        self.send_message_from_author_for_request_confirmed(request_product.user, request_product.product.contact)
        request_product.product.confirm_deliver()

    def _confirm_received(self, post, request_product):
        self.send_message_to_author_for_product_received_confirmed(request_product.product.author)
        request_product.product.confirm_received()

    def _cancel_request(self, post, request_product):
        request_product.cancel()

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        post = request.POST.copy()
        request_product = RequestProduct.objects.filter(id=self.id).first()
        title = "Detalle de la solicitud del producto {}".format(request_product.product.name)
        if request_product.user.id != request.user.id and request_product.product.author.id != request.user.id:
            return HttpResponseForbidden()
        if post["action_request"] == "confirm_deliver" and request_product.product.author.id == request.user.id:
            self._confirm_deliver(post, request_product)
        elif post["action_request"] == "confirm_received" and request_product.user.id == request.user.id:
            self._confirm_received(post, request_product)
        elif post["action_request"] == "cancel_request":
            self._cancel_request(post, request_product)
            return redirect(reverse("product_detail", kwargs={"slug": request_product.product.slug}))
        return render(request, "panel/requests/detail.html", locals())
