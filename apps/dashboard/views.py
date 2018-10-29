from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib import messages
from apps.products.models import ReportProduct, Product
from apps.events.models import Event
from apps.events.forms import EventForm
from django.http import HttpResponseForbidden
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from datetime import datetime

# Create your views here.
class RevitionIndexView(View):

    @method_decorator(staff_member_required)
    def get(self, request, *args, **kwargs):
        return render(request, "", locals())


class RevitionProductIndexView(View):

    @property
    def product_id(self):
        if "product_id" in self.kwargs:
            return self.kwargs["product_id"]
        return None


    @method_decorator(staff_member_required)
    def get(self, request, *args, **kwargs):
        reports_product = ReportProduct.objects.filter(product__visible=False).all()
        return render(request, "dashboard/revition/products/index.html", locals())


    @method_decorator(staff_member_required)
    def post(self, request, *args, **kwargs):
        reports_product = ReportProduct.objects.filter(product__visible=False).all()
        product_id = self.product_id
        if product_id is None:
            return HttpResponseForbidden()
        product = Product.objects.filter(id=product_id).first()
        product.visible = False
        product.save()
        messages.success(request, "El producto ha sido deshabilitado con éxito")
        return render(request, "dashboard/revition/products/index.html", locals())

class RevitionImageIndexView(View):

    @method_decorator(staff_member_required)
    def get(self, request, *args, **kwargs):
        return render(request, "", locals())


class EventsDashboardView(View):

    @method_decorator(staff_member_required)
    def get(self, request, *args, **kwargs):
        events = Event.objects.filter(date_event__gte=datetime.now()).all()
        return render(request, "dashboard/events/index.html", locals())


class EventsDashboardCreateView(View):

    @method_decorator(staff_member_required)
    def get(self, request, *args, **kwargs):
        form = EventForm()
        return render(request, "dashboard/events/create.html", locals())


    @method_decorator(staff_member_required)
    def post(self, request, *args, **kwargs):
        post = request.POST.copy()
        form = EventForm(post)
        if form.is_valid():
            form.save()
            return redirect(reverse("events_index_dashboard"))
        else:
            for e in form.errors:
                messages.error(request, e)
        return render(request, "dashboard/events/create.html", locals())


class EventsDashboardEditView(View):

    @property
    def id(self):
        if "id" in self.kwargs:
            return self.kwargs["id"]
        return None

    @method_decorator(staff_member_required)
    def get(self, request, *args, **kwargs):
        id = self.id
        if id is None:
            return HttpResponseForbidden()
        event = Event.objects.filter(id=self.id).first()
        if event is None:
            form = EventForm()
        else:
            form = EventForm(instance=event)
        return render(request, "dashboard/events/create.html", locals())


    @method_decorator(staff_member_required)
    def post(self, request, *args, **kwargs):
        id = self.id
        if id is None:
            return HttpResponseForbidden()
        event = Event.objects.filter(id=self.id).first()
        post = self.request.POST.copy()
        if event is None:
            form = EventForm(post)
        else:
            form = EventForm(post, instance=event)
        if form.is_valid():
            form.save()
            return redirect(reverse("events_index_dashboard"))
        else:
            for e in form.errors:
                messages.error(request, e)
        return render(request, "dashboard/events/create.html", locals())
